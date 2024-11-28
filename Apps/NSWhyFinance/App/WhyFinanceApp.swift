//
//  WhyFinanceApp.swift
//  WhyFinanceApp
//
//  Created by Alessio Giordano on 26/11/24.
//

import SwiftUI

@main
struct WhyFinanceApp: App {
    var body: some Scene {
        #if os(macOS)
        Window("Why Finance", id: "main") {
            if #available(macOS 15.0, *) {
                ContentView()
                    .windowMinimizeBehavior(.disabled)
                    .windowResizeBehavior(.disabled)
                    .windowFullScreenBehavior(.disabled)
                    .frame(width: 260, height: 340)
            } else {
                ContentView().frame(width: 260, height: 340)
            }
        }
        .windowStyle(.hiddenTitleBar)
        .windowToolbarStyle(.unifiedCompact)
        .defaultSize(width: 260, height: 340)
        .windowResizability(.contentSize)
        .defaultPosition(.center)
        .commands {
            CommandGroup(after: .appSettings) {
                Button("Hard Reset") {
                    UserDefaults.standard.removeObject(forKey: "ticker")
                    UserDefaults.standard.removeObject(forKey: "email")
                    UserDefaults.standard.removeObject(forKey: "host")
                }
            }
        }
        #else
        WindowGroup {
            ContentView()
        }
        #endif
    }
}
