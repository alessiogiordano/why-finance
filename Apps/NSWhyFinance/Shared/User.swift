//
//  User.swift
//  NSWhyFinance
//
//  Created by Alessio Giordano on 23/12/24.
//

import Foundation
import DeviceCheck

struct User: StringCodable {
    let host: String?
    var baseURL: URL { .whyFinanceBaseURL(host: host) ?? .whyFinanceBaseURL }
    let deviceId: String
    let ticker: String
    let deviceToken: String?
    let highValue: Float?
    let lowValue: Float?
    
    static func generateDeviceId() async -> String {
        if DCDevice.current.isSupported,
           let data = try? await DCDevice.current.generateToken(),
           let deviceId = String(data: data, encoding: .utf8) {
            return deviceId
        } else {
            if let deviceId = UserDefaults.standard.string(forKey: .userDefaultsDeviceIdKey) {
                return deviceId
            } else {
                let randomId = UUID().uuidString
                UserDefaults.standard.set(randomId, forKey: .userDefaultsDeviceIdKey)
                return randomId
            }
        }
    }
    
    init(host: String?, deviceId: String, ticker: String, deviceToken: String? = nil, highValue: Float?, lowValue: Float?) {
        self.host = host
        self.deviceId = deviceId
        self.ticker = ticker
        self.deviceToken = deviceToken ?? UserDefaults.standard.string(forKey: .userDefaultsDeviceTokenKey)
        self.highValue = highValue
        self.lowValue = lowValue
    }
    
    init?(userDefaults: UserDefaults) {
        guard let user = (User?).init(rawValue: UserDefaults.standard.string(forKey: .userDefaultsUserKey)) ?? nil
        else { return nil }
        self = user
    }
    
    func save() {
        UserDefaults.standard.set((self as User?).rawValue, forKey: .userDefaultsUserKey)
    }
}

extension User {
    func put() async throws {
        var request = URLRequest(url: baseURL.appending(path: "users", directoryHint: .isDirectory)
                                             .appending(path: deviceId, directoryHint: .notDirectory))
        request.httpMethod = "PUT"
        let encoder = JSONEncoder()
        encoder.keyEncodingStrategy = .convertToSnakeCase
        request.httpBody = try? encoder.encode(self)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        return try await withCheckedThrowingContinuation { continuation in
            Task.detached(priority: .background) {
                do {
                    let (_, response) = try await URLSession.shared.data(for: request)
                    guard (response as? HTTPURLResponse)?.statusCode == 204 else {
                        throw URLError(.badServerResponse)
                    }
                    continuation.resume()
                } catch {
                    continuation.resume(throwing: error)
                }
            }
        }
    }
    @discardableResult
    func delete() async throws -> Self? {
        var request = URLRequest(url: baseURL.appending(path: "users", directoryHint: .isDirectory)
                                             .appending(path: deviceId, directoryHint: .notDirectory))
        request.httpMethod = "DELETE"
        return try await withCheckedThrowingContinuation { continuation in
            Task.detached(priority: .background) {
                do {
                    let (_, response) = try await URLSession.shared.data(for: request)
                    guard (response as? HTTPURLResponse)?.statusCode == 204 else {
                        throw URLError(.badServerResponse)
                    }
                    continuation.resume(returning: nil)
                } catch {
                    continuation.resume(throwing: error)
                }
            }
        }
    }
}

extension User {
    func getStock(aggregate: Stock.Aggregate? = .none) -> Stock {
        .init(baseURL: self.baseURL, ticker: self.ticker, price: nil, timestamp: nil, aggregate: aggregate)
    }
}

extension User {
    func withDeviceToken(_ token: String) -> User {
        return .init(host: self.host,
                     deviceId: self.deviceId,
                     ticker: self.ticker,
                     deviceToken: token,
                     highValue: self.highValue,
                     lowValue: self.lowValue)
    }
}
