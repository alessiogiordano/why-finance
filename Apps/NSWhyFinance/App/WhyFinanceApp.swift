//
//  WhyFinanceApp.swift
//  WhyFinanceApp
//
//  Created by Alessio Giordano on 26/11/24.
//

import SwiftUI

@main
struct WhyFinanceApp: App {
    #if os(macOS)
    @NSApplicationDelegateAdaptor private var appData: AppData
    #else
    @UIApplicationDelegateAdaptor private var appData: AppData
    #endif
    
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
                    appData.reset()
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
