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
                        TextField("Ticker", text: $tickerField)
                            .textCase(tickerField.isEmpty ? .none : .uppercase)
                    }
                } else {
                    // User Update and Deletion
                    Section {
                        TextField("Ticker", text: $tickerField)
                            .textCase(tickerField.isEmpty ? .none : .uppercase)
                    }
                    Section {
                        LabelledText(label: "Host", value: hostField)
                        LabelledText(label: "Email", value: emailField)
                        Button("Cancella tutti i dati utente", role: .destructive) {
                            withHTTPTask {
                                try await deleteTickerSubscription(for: email, at: host)
                            } then: {
                                self.ticker = ""
                                self.email = ""
                                self.host = ""
                                dismiss()
                            }
                        }
                    }.lineLimit(1)
                }
            }
            .textInputAutocapitalization(.never)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Annulla") {
                        httpTask?.cancel()
                        dismiss()
                    }
                }
                ToolbarItem(placement: .confirmationAction) {
                    if httpTask != nil {
                        ProgressView()
                    } else {
                        Button("Fine") {
                            withHTTPTask {
                                try await putTickerSubscription(for: emailField, of: tickerField, at: hostField)
                            } then: {
                                email = emailField
                                ticker = tickerField
                                dismiss()
                            }
                        }.disabled(emailField.isEmpty || tickerField.isEmpty || !hasModifiedContent)
                    }
                    
                }
            }
            .toolbarTitleDisplayMode(.inline)
            .navigationTitle("Configurazione")
        }
        .presentationDetents([.medium])
        .interactiveDismissDisabled(hasModifiedContent)
        .onAppear {
            hostField = URL.whyFinanceBaseURL.absoluteString
            emailField = email
            tickerField = ticker
        }
        .disabled(httpTask != nil)
        .alert("Impossibile connettersi al servizio Why Finance", isPresented: $httpErrorAlert) {
            Button("OK", role: .cancel) {
                httpErrorAlert = false
            }
        }
    }
    
    func withHTTPTask(action: @escaping  () async throws -> (), then mainActor: @escaping () -> ()) {
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
    
    func putTickerSubscription(for email: String, of ticker: String, at host: String? = nil) async throws {
        let baseURL: URL
        if let host, !host.isEmpty {
            if host.hasPrefix("http://") || host.hasPrefix("https://") {
                if let url = URL(string: host) {
                    baseURL = url
                } else {
                    throw URLError(.badURL)
                }
            } else {
                if let url = URL(string: "http://" + host) {
                    baseURL = url
                } else {
                    throw URLError(.badURL)
                }
            }
        } else {
            baseURL = .whyFinanceBaseURL
        }
        var request = URLRequest(url: baseURL.appending(path: "users", directoryHint: .isDirectory).appending(path: email, directoryHint: .notDirectory))
        request.httpMethod = "PUT"
        request.httpBody = ticker.uppercased().data(using: .utf8)
        let (_, response) = try await URLSession.shared.data(for: request)
        guard (response as? HTTPURLResponse)?.statusCode == 204 else {
            throw URLError(.badServerResponse)
        }
    }
    func deleteTickerSubscription(for email: String, at host: String? = nil) async throws {
        let baseURL: URL
        if let host, !host.isEmpty {
            if host.hasPrefix("http://") || host.hasPrefix("https://") {
                if let url = URL(string: host) {
                    baseURL = url
                } else {
                    throw URLError(.badURL)
                }
            } else {
                if let url = URL(string: "http://" + host) {
                    baseURL = url
                } else {
                    throw URLError(.badURL)
                }
            }
        } else {
            baseURL = .whyFinanceBaseURL
        }
        var request = URLRequest(url: baseURL.appending(path: "users", directoryHint: .isDirectory).appending(path: email, directoryHint: .notDirectory))
        request.httpMethod = "DELETE"
        let (_, response) = try await URLSession.shared.data(for: request)
        guard (response as? HTTPURLResponse)?.statusCode == 204 else {
            throw URLError(.badServerResponse)
        }
    }
}
