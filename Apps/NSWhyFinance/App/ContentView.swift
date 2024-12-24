//
//  ContentView.swift
//  WhyFinanceApp
//
//  Created by Alessio Giordano on 26/11/24.
//

import UserNotifications
import SwiftUI
import TipKit

struct ContentView: View {
    @State var sheet = false
    //
    @EnvironmentObject private var appData: AppData
    //
    @State var offset: CGFloat = 0.0
    //
    var body: some View {
        NavigationStack {
            ScrollView {
                VerticalPositionReader(position: $offset, coordinateSpace: .named("ScrollView"))
            }
            .overlay {
                WidgetView()
                    .systemSmallWidget()
                    .offset(y: offset * -1)
                    .environment(\.colorScheme, .light)
                    .allowsHitTesting(false)
                    #if os(macOS)
                    .ignoresSafeArea(.all)
                    .offset(y: -12) // Title bar
                    #endif
            }
            .coordinateSpace(.named("ScrollView"))
            .scrollContentBackground(.hidden)
            .refreshable {
                try? await appData.refresh()
            }
            .onChange(of: appData, initial: true) {
                ConfigurationViewTip.isPresented = (appData.user == nil)
            }
            .onAppear {
                try? Tips.resetDatastore()
                try? Tips.configure()
            }
            #if os(iOS)
            .toolbar {
                ToolbarItemGroup(placement: .bottomBar) {
                    Button {
                        sheet.toggle()
                    } label: {
                        Label("Configura", systemImage: "info.circle")
                    }
                    .buttonStyle(.plain)
                    .popoverTip(ConfigurationViewTip())
                    Spacer()
                }
            }
            .toolbarBackground(.hidden, for: .navigationBar, .bottomBar)
            #endif
            #if os(macOS)
            .overlay(alignment: .bottom) {
                HStack {
                    Button {
                        sheet.toggle()
                    } label: {
                        Label("Configura", systemImage: "info.circle")
                    }.popoverTip(ConfigurationViewTip())
                    Spacer()
                    Button {
                        Task {
                            try? await appData.refresh()
                        }
                    } label: {
                        Label("Ricarica", systemImage: "arrow.clockwise")
                    }
                }.buttonStyle(.plain).labelStyle(.iconOnly).padding()
            }
            #endif
            .sheet(isPresented: $sheet) {
                ConfigurationView()
            }
            .background {
                LinearGradient(colors: [.whyFinanceLight, .whyFinanceDark],
                               startPoint: .top, endPoint: .bottom)
                    #if os(iOS)
                    .overlay(.bar)
                    #endif
                    #if os(macOS)
                    .opacity(0.5)
                    #endif
                    .ignoresSafeArea(.all)
            }
            #if os(macOS)
            .visualEffect(material: .hudWindow, ignoresSafeArea: .all)
            #endif
            .navigationTitle("Why Finance")
            .toolbarTitleDisplayMode(.inline)
        }
        .environment(\.colorScheme, .dark)
        .environment(\.whyFinanceBaseURL, .whyFinanceBaseURL(host: appData.user?.host) ?? .whyFinanceBaseURL)
        .task {
            let center = UNUserNotificationCenter.current()
            //let settings = await center.notificationSettings()
            //if (settings.authorizationStatus == .authorized) ||
            //      (settings.authorizationStatus == .provisional) { return }
            do {
                try await center.requestAuthorization(options: [.alert, .sound, .badge, .provisional])
            } catch {
                print("Unexpectedly denied permission to receive notifications")
            }
            #if os(macOS)
            NSApplication.shared.registerForRemoteNotifications()
            #else
            UIApplication.shared.registerForRemoteNotifications()
            #endif
        }
    }
}

struct ConfigurationViewTip: Tip {
    var title: Text {
        Text("Configura il widget")
    }
    var message: Text? {
        Text("Premi questo pulsante per configurare il widget con il ticker da monitorare e altre opzioni")
    }
    var image: Image? {
        Image(systemName: "info.circle")
    }
    //
    @Parameter static var isPresented: Bool = false
    var rules: [Rule] {
        [ #Rule(Self.$isPresented) { $0 == true } ]
    }
}
