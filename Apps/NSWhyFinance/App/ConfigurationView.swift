//
//  ConfigurationView.swift
//  WhyFinanceApp
//
//  Created by Alessio Giordano on 28/11/24.
//

import SwiftUI

struct ConfigurationView: View {
    @EnvironmentObject private var appData: AppData
    //
    @State var hostField: String = ""
    @State var tickerField: String = ""
    ///
    @State var shouldAverageValues = false
    @State var stockAverageCount = 2
    ///
    @State var shouldAlertHighThreshold: Bool = false
    @State var highThreshold: Float = 150.0
    @State var shouldAlertLowThreshold: Bool = false
    @State var lowThreshold: Float = 25.0
    //
    @Environment(\.dismiss) var dismiss
    @State var httpTask: Task<Void,Never>? = nil
    @State var httpErrorAlert = false
    //
    var invalidAlertInterval: Bool {
        shouldAlertLowThreshold && shouldAlertHighThreshold && highThreshold < lowThreshold
    }
    var hasModifiedContent: Bool {
        if appData.user?.ticker != tickerField { return true }
        if shouldAlertHighThreshold != (appData.user?.highValue != nil) { return true }
        if shouldAlertLowThreshold != (appData.user?.lowValue != nil) { return true }
        if highThreshold != appData.user?.lowValue { return true }
        if lowThreshold != appData.user?.lowValue { return true }
        return false
    }
    //
    var options: some View {
        #if os(macOS)
        Section {
            Toggle(isOn: $shouldAverageValues) {
                LabeledContent("Media il valore degli ultimi") {
                    Stepper {
                        Text("\(Int(stockAverageCount)) campioni")
                            .monospacedDigit()
                            .offset(x: -4)
                    } onIncrement: {
                        stockAverageCount += 1
                    } onDecrement: {
                        stockAverageCount = max(2, stockAverageCount - 1)
                    }
                }
            }
            Toggle(isOn: $shouldAlertHighThreshold) {
                LabeledContent("Notifica se il valore sale sopra") {
                    TextField("", value: $highThreshold, format: .number)
                    Stepper {
                        //
                    } onIncrement: {
                        highThreshold += 1
                    } onDecrement: {
                        highThreshold = max(max(0, highThreshold - 1), shouldAlertLowThreshold ? lowThreshold : 0)
                    }.fixedSize()
                }
            }
            Toggle(isOn: $shouldAlertLowThreshold) {
                LabeledContent("Notifica se il valore scende sotto") {
                    TextField("", value: $lowThreshold, format: .number)
                    Stepper {
                        //
                    } onIncrement: {
                        lowThreshold += 1
                    } onDecrement: {
                        lowThreshold = min(max(0, lowThreshold - 1), shouldAlertHighThreshold ? highThreshold : .greatestFiniteMagnitude)
                    }.fixedSize()
                }
            }
        }
        #else
        Group {
            Toggle(isOn: $shouldAverageValues) {
                Text("Calcola la media")
            }
            if shouldAverageValues {
                Stepper {
                    Text("Ultimi \(Int(stockAverageCount)) campioni")
                        .monospacedDigit()
                } onIncrement: {
                    stockAverageCount += 1
                } onDecrement: {
                    stockAverageCount = max(2, stockAverageCount - 1)
                }
            }
            //
            Toggle(isOn: $shouldAlertHighThreshold) {
                Text("Notifica quando sopra la soglia")
            }
            if shouldAlertHighThreshold {
                HStack {
                    TextField("", value: $highThreshold, format: .number)
                        .foregroundStyle(.secondary)
                        .keyboardType(.decimalPad)
                    Stepper {
                        //
                    } onIncrement: {
                        highThreshold += 1
                    } onDecrement: {
                        highThreshold = max(max(0, highThreshold - 1), shouldAlertLowThreshold ? lowThreshold : 0)
                    }.fixedSize()
                }
            }
            //
            Toggle(isOn: $shouldAlertLowThreshold) {
                Text("Notifica quando sotto la soglia")
            }
            if shouldAlertLowThreshold {
                HStack {
                    TextField("", value: $lowThreshold, format: .number)
                        .foregroundStyle(.secondary)
                        .keyboardType(.decimalPad)
                    Stepper {
                        //
                    } onIncrement: {
                        lowThreshold += 1
                    } onDecrement: {
                        lowThreshold = min(max(0, lowThreshold - 1), shouldAlertHighThreshold ? highThreshold : .greatestFiniteMagnitude)
                    }.fixedSize()
                }
            }
        }
        #endif
    }
    //
    var body: some View {
        NavigationStack {
            Form {
                if appData.user == nil {
                    // User Registration
                    Section {
                        TextField("Host", text: $hostField)
                            .textContentType(.URL)
                    }
                    Section {
                        //TextField("Email", text: $emailField)
                         //   .textContentType(.emailAddress)
                        #if os(macOS)
                        LabeledContent("Ticker") {
                            TextField("Ticker", text: $tickerField)
                                .textCase(.uppercase)
                                .labelsHidden()
                        }
                        options
                        #else
                        TextField("Ticker", text: $tickerField)
                            .textCase(tickerField.isEmpty ? .none : .uppercase)
                        options
                        #endif
                    }
                } else {
                    // User Update and Deletion
                    Section {
                        
                        #if os(macOS)
                        LabeledContent("Ticker") {
                            TextField("Ticker", text: $tickerField)
                                .textCase(.uppercase)
                                .labelsHidden()
                        }
                        //
                        options
                        Divider()
                        //
                        LabeledText(label: "Host", value: appData.user?.host ?? "")
                        LabeledText(label: "Device ID", value: appData.user?.deviceId ?? "")
                        #else
                        TextField("Ticker", text: $tickerField)
                            .textCase(tickerField.isEmpty ? .none : .uppercase)
                        options
                        #endif
                    }
                    #if os(macOS)
                    #else
                    Section {
                        LabeledText(label: "Host", value: appData.user?.host ?? "")
                        LabeledText(label: "Device ID", value: appData.user?.deviceId ?? "")
                        Button("Cancella tutti i dati utente", role: .destructive, action: cancel)
                    }.lineLimit(1)
                    #endif
                }
            }
            #if os(iOS)
            .textInputAutocapitalization(.never)
            #endif
            .toolbar {
                #if os(macOS)
                if appData.user != nil {
                    ToolbarItem(placement: .destructiveAction) {
                        Button("Cancella tutti i dati utente", role: .destructive, action: cancel)
                    }
                }
                #endif
                ToolbarItem(placement: .cancellationAction) {
                    Button("Annulla") {
                        httpTask?.cancel()
                        dismiss()
                    }
                }
                ToolbarItem(placement: .confirmationAction) {
                    if httpTask != nil {
                        #if os(macOS)
                        Button("Fine") {}.disabled(true).opacity(0).overlay {
                            ProgressView().scaleEffect(0.5)
                        }
                        #else
                        ProgressView()
                        #endif
                    } else {
                        Button("Fine", action: done)
                            .disabled(tickerField.isEmpty || !hasModifiedContent || invalidAlertInterval)
                    }
                }
            }
            #if os(iOS)
            .toolbarTitleDisplayMode(.inline)
            #endif
            .navigationTitle("Configurazione")
            #if os(macOS)
            .padding()
            #endif
        }
        .presentationDetents([.medium])
        .interactiveDismissDisabled(hasModifiedContent)
        .onAppear {
            hostField = appData.user?.host ?? URL.whyFinanceBaseURL.absoluteString
            tickerField = appData.user?.ticker ?? ""
            if case .average(let last) = appData.stock?.aggregate {
                shouldAverageValues = true
                stockAverageCount = last
            } else {
                shouldAverageValues = false
                stockAverageCount = 2
            }
            shouldAlertHighThreshold = appData.user?.highValue != nil
            highThreshold = appData.user?.highValue ?? 150.0
            shouldAlertLowThreshold = appData.user?.lowValue != nil
            lowThreshold = appData.user?.lowValue ?? 25.0
        }
        .disabled(httpTask != nil)
        .alert("Impossibile connettersi al servizio Why Finance", isPresented: $httpErrorAlert) {
            Button("OK", role: .cancel) {
                httpErrorAlert = false
            }
        }
        #if os(macOS)
        .frame(minWidth: 420)
        #endif
    }
    
    private func done() {
        withHTTPTask {
            let deviceId = await User.generateDeviceId()
            let user = User(host: hostField, deviceId: deviceId, ticker: tickerField, highValue: shouldAlertHighThreshold ? highThreshold : nil, lowValue: shouldAlertLowThreshold ? lowThreshold : nil)
            try await appData.updateUser(user)
            if shouldAverageValues {
                let stock = user.getStock(aggregate: .average(last: Int(stockAverageCount)))
                appData.updateStock(stock)
            } else {
                let stock = user.getStock()
                appData.updateStock(stock)
            }
            try await appData.refresh()
        } then: {
            dismiss()
        }
    }
    
    private func cancel() {
        withHTTPTask {
            try await appData.delete()
        } then: {
            dismiss()
        }
    }
    
    private func withHTTPTask(action: @escaping  () async throws -> (), then mainActor: @escaping () -> ()) {
        self.httpTask = Task.detached {
            do {
                try await action()
                await MainActor.run {
                    mainActor()
                }
            } catch {
                if !Task.isCancelled {
                    await MainActor.run {
                        httpErrorAlert = true
                        self.httpTask = nil
                    }
                }
            }
        }
    }
}
