//
//  ContentView.swift
//  WhyFinanceApp
//
//  Created by Alessio Giordano on 26/11/24.
//

import SwiftUI
import TipKit

struct ContentView: View {
    @State var sheet = false
    //
    @AppStorage("host") var host = ""
    @AppStorage("email") var email = ""
    @AppStorage("ticker") var ticker = ""
    //
    @State var id: UUID = .init()
    @State var offset: CGFloat = 0.0
    //
    var body: some View {
        NavigationStack {
            ScrollView {
                VerticalPositionReader(position: $offset, coordinateSpace: .named("ScrollView"))
            }
            .overlay {
                WidgetView(ticker: ticker)
                    .systemSmallWidget()
                    .id(id.uuidString)
                    .offset(y: offset * -1)
                    .environment(\.colorScheme, .light)
                    .allowsHitTesting(false)
                    #if os(macOS)
                    .ignoresSafeArea(.all)
                    .offset(y: -12) // Title barc
                    #endif
            }
            .coordinateSpace(.named("ScrollView"))
            .scrollContentBackground(.hidden)
            .refreshable {
                id = .init()
            }
            .onChange(of: ticker, initial: true) { oldValue, newValue in
                if newValue != oldValue {
                    self.id = .init()
                }
                ConfigurationViewTip.isPresented = newValue.isEmpty
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
                        id = .init()
                    } label: {
                        Label("Ricarica", systemImage: "arrow.clockwise")
                    }
                }.buttonStyle(.plain).labelStyle(.iconOnly).padding()
            }
            #endif
            .sheet(isPresented: $sheet) {
                ConfigurationView(host: $host, email: $email, ticker: $ticker)
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
        .environment(\.whyFinanceBaseURL, .whyFinanceBaseURL(host: host) ?? .whyFinanceBaseURL)
    }
}

struct ConfigurationViewTip: Tip {
    var title: Text {
        Text("Configura il widget")
    }
    var message: Text? {
        Text("Premi questo pulsante per configurare il widget con un indirizzo email ed il ticker da monitorare")
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
