//
//  AppData.swift
//  NSWhyFinance
//
//  Created by Alessio Giordano on 23/12/24.
//

import Foundation

class AppData: NSObject, ObservableObject {
    @Published private(set) var user: User?
    @Published private(set) var stock: Stock?
    
    override init() {
        super.init()
        self.user = .init(userDefaults: .standard)
        self.stock = .init(userDefaults: .standard)
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(userDefaultsDidChange(_:)),
            name: UserDefaults.didChangeNotification,
            object: nil
        )
    }
    deinit {
        NotificationCenter.default.removeObserver(self, name: UserDefaults.didChangeNotification, object: nil)
    }
    
    @objc func userDefaultsDidChange(_ notification: Notification) {
        return // I don't need this
        //DispatchQueue.main.async {
        //    self.user = .init(userDefaults: .standard)
        //    self.stock = .init(userDefaults: .standard)
        //}
    }
}

extension AppData {
    func refresh() async throws {
        if let refreshed = try? await stock?.refreshed() {
            refreshed.save()
            await MainActor.run {
                self.stock = refreshed
            }
        }
    }
    ///
    func updateDeviceToken(_ token: String) async throws {
        if let user {
            let updatedUser = user.withDeviceToken(token)
            try await updatedUser.put()
            updatedUser.save()
            await MainActor.run {
                self.user = updatedUser
            }
        }
    }
    ///
    func updateUser(_ user: User) async throws {
        let previousTicker = self.user?.ticker
        try await user.put()
        user.save()
        await MainActor.run {
            self.user = user
        }
        if previousTicker != user.ticker {
            let stock = user.getStock()
            stock.save()
            await MainActor.run {
                self.stock = stock
            }
        }
    }
    @MainActor
    func updateStock(_ stock: Stock) {
        stock.save()
        self.stock = stock
    }
    ///
    func delete() async throws {
        try await self.user?.delete()
        await self.reset()
    }
    @MainActor
    func reset() {
        self.user = nil
        UserDefaults.standard.removeObject(forKey: .userDefaultsUserKey)
        self.stock = nil
        UserDefaults.standard.removeObject(forKey: .userDefaultsStockKey)
    }
}
