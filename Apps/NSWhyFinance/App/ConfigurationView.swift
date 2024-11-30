//
//  ConfigurationView.swift
//  WhyFinanceApp
//
//  Created by Alessio Giordano on 28/11/24.
//

import SwiftUI

struct ConfigurationView: View {
    @Binding var host: String
    @Binding var email: String
    @Binding var ticker: String
    //
    @State var hostField: String = ""
    @State var emailField: String = ""
    @State var tickerField: String = ""
    //
    @Environment(\.dismiss) var dismiss
    @State var httpTask: Task<Void,Never>? = nil
    @State var httpErrorAlert = false
    //
    var hasModifiedContent: Bool {
        (email != emailField) || (ticker != tickerField)
    }
    //
    var body: some View {
        NavigationStack {
            Form {
                if email.isEmpty {
                    // User Registration
                    Section {
                        TextField("Host", text: $hostField)
                            .textContentType(.URL)
                    }
                    Section {
                        TextField("Email", text: $emailField)
                            .textContentType(.emailAddress)
                        #if os(macOS)
                        LabeledContent("Ticker") {
                            TextField("Ticker", text: $tickerField)
                                .textCase(.uppercase)
                                .labelsHidden()
                        }
                        #else
                        TextField("Ticker", text: $tickerField)
                            .textCase(tickerField.isEmpty ? .none : .uppercase)
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
                        Divider()
                        LabeledText(label: "Host", value: host)
                        LabeledText(label: "Email", value: email)
                        #else
                        TextField("Ticker", text: $tickerField)
                            .textCase(tickerField.isEmpty ? .none : .uppercase)
                        #endif
                    }
                    #if os(macOS)
                    #else
                    Section {
                        LabeledText(label: "Host", value: host)
                        LabeledText(label: "Email", value: email)
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
                if !email.isEmpty {
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
                            .disabled(emailField.isEmpty || tickerField.isEmpty || !hasModifiedContent)
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
            hostField = host.isEmpty ? URL.whyFinanceBaseURL.absoluteString : host
            emailField = email
            tickerField = ticker
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
            try await putTickerSubscription(for: emailField, of: tickerField, at: hostField)
        } then: {
            email = emailField
            ticker = tickerField
            host = hostField
            dismiss()
        }
    }
    
    private func cancel() {
        withHTTPTask {
            try await deleteTickerSubscription(for: email, at: host)
        } then: {
            self.ticker = ""
            self.email = ""
            self.host = ""
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
    
    private func putTickerSubscription(for email: String, of ticker: String, at host: String? = nil) async throws {
        guard let baseURL = URL.whyFinanceBaseURL(host: host) else { throw URLError(.badURL) }
        var request = URLRequest(url: baseURL.appending(path: "users", directoryHint: .isDirectory).appending(path: email, directoryHint: .notDirectory))
        request.httpMethod = "PUT"
        request.httpBody = ticker.uppercased().data(using: .utf8)
        let (_, response) = try await URLSession.shared.data(for: request)
        guard (response as? HTTPURLResponse)?.statusCode == 204 else {
            throw URLError(.badServerResponse)
        }
    }
    private func deleteTickerSubscription(for email: String, at host: String? = nil) async throws {
        guard let baseURL = URL.whyFinanceBaseURL(host: host) else { throw URLError(.badURL) }
        var request = URLRequest(url: baseURL.appending(path: "users", directoryHint: .isDirectory).appending(path: email, directoryHint: .notDirectory))
        request.httpMethod = "DELETE"
        let (_, response) = try await URLSession.shared.data(for: request)
        guard (response as? HTTPURLResponse)?.statusCode == 204 else {
            throw URLError(.badServerResponse)
        }
    }
}
