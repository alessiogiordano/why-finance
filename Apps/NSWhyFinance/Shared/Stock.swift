//
//  Stock.swift
//  NSWhyFinance
//
//  Created by Alessio Giordano on 23/12/24.
//

import Foundation

struct Stock: StringCodable {
    let baseURL: URL
    let ticker: String
    let price: Float?           // Data is nil before the very first fetch
    let timestamp: Date?        // Data is nil before the very first fetch
    let aggregate: Aggregate?
    enum Aggregate: Codable {
        case average(last: Int)
    }
    
    init(baseURL: URL, ticker: String, price: Float?, timestamp: Date?, aggregate: Aggregate?) {
        self.baseURL = baseURL
        self.ticker = ticker
        self.price = price
        self.timestamp = timestamp
        self.aggregate = aggregate
    }
    
    init?(userDefaults: UserDefaults) {
        guard let stock = (Stock?).init(rawValue: UserDefaults.standard.string(forKey: .userDefaultsStockKey)) ?? nil
        else { return nil }
        self = stock
    }
    
    func save() {
        UserDefaults.standard.set((self as Stock?).rawValue, forKey: .userDefaultsStockKey)
    }
}

extension Stock {
    func refreshed() async throws -> Stock {
        var url = baseURL.appending(path: "stocks", directoryHint: .isDirectory)
                         .appending(path: ticker, directoryHint: .notDirectory)
        if case .average(let last) = aggregate {
            url.append(queryItems: [.init(name: "avg", value: "\(last)")])
        }
        return try await withCheckedThrowingContinuation { continuation in
            Task.detached(priority: .background) { [self] in
                do {
                    let value = try String(contentsOf: url)
                    guard let price = Float(value) else { throw URLError(.badServerResponse) }
                    continuation.resume(returning: .init(baseURL: self.baseURL,
                                                         ticker: self.ticker,
                                                         price: price,
                                                         timestamp: Date(),
                                                         aggregate: self.aggregate))
                } catch {
                    continuation.resume(throwing: error)
                }
            }
        }
    }
    func withExternalUpdate(ticker: String, price: Float) async throws -> Stock {
        guard ticker == self.ticker, self.aggregate == nil else {
            // Data is not useful, but still signals the need to update
            return try await self.refreshed()
        }
        return .init(baseURL: self.baseURL,
                     ticker: ticker,
                     price: price,
                     timestamp: Date(),
                     aggregate: nil)
    }
}
