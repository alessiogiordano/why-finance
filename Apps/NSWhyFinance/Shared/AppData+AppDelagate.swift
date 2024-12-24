//
//  AppData+AppDelagate.swift
//  NSWhyFinance
//
//  Created by Alessio Giordano on 23/12/24.
//

fileprivate extension AppData {
    func didRegisterForRemoteNotifications(with deviceToken: Data) {
        let token = deviceToken.map { String(format: "%02x", $0) }.joined()
        UserDefaults.standard.set(token, forKey: .userDefaultsDeviceTokenKey)
        Task.detached(priority: .background) {
            try? await self.updateDeviceToken(token)
        }
    }
    func didReceiveRemoteNotification(userInfo: [AnyHashable : Any],
                                      then completionHandler: (() -> ())? = nil) {
        if let ticker = userInfo["ticker"] as? String,
           let price = userInfo["price"] as? Float {
            Task.detached(priority: .background) {
                guard let newStock = try? await self.stock?.withExternalUpdate(ticker: ticker, price: price)
                else { return completionHandler?() }
                await self.updateStock(newStock)
                completionHandler?()
            }
        }
    }
}

#if os(macOS)
import AppKit
extension AppData: NSApplicationDelegate {
    func application(
        _ application: NSApplication,
        didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data
    ) {
        didRegisterForRemoteNotifications(with: deviceToken)
    }
    func application(
        _ application: NSApplication,
        didReceiveRemoteNotification userInfo: [String : Any]
    ) {
        didReceiveRemoteNotification(userInfo: userInfo)
    }
}
#else
import UIKit
extension AppData: UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data
    ) {
        didRegisterForRemoteNotifications(with: deviceToken)
    }
    func application(
        _ application: UIApplication,
        didReceiveRemoteNotification userInfo: [AnyHashable : Any],
        fetchCompletionHandler completionHandler: @escaping (UIBackgroundFetchResult) -> Void
    ) {
        didReceiveRemoteNotification(userInfo: userInfo, then: { completionHandler(.newData) })
    }
}
#endif
