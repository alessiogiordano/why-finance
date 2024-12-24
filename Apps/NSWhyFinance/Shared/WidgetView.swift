import SwiftUI

struct WidgetView: View {
    @State var value: Float?
    @Environment(\.whyFinanceBaseURL) var baseURL
    @EnvironmentObject private var appData: AppData
    
    let provider: WidgetProvider
    enum WidgetProvider {
        case userDefaults, ticker(String)
    }
    init(provider: WidgetProvider = .userDefaults) {
        self.provider = provider
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            if case .ticker(let string) = provider {
                Text(string).font(.headline)
            } else if case .userDefaults = provider, let stock = appData.stock {
                Text(stock.ticker).font(.headline)
            } else {
                Text("-----").font(.headline)
                    .redacted(reason: .placeholder)
            }
            //
            Spacer().frame(maxWidth: .infinity)
            if let value {
                Text(String(format: "%.3f", value)).font(.largeTitle)
                    .minimumScaleFactor(0.1)
            } else if case .userDefaults = provider,
                      let stock = appData.stock, let price = stock.price {
                Text(String(format: "%.3f", price)).font(.largeTitle)
                    .minimumScaleFactor(0.1)
            } else {
                Text("---.--").font(.largeTitle)
                    .redacted(reason: .placeholder)
            }
        }
        .foregroundStyle(.ultraThickMaterial)
        .onChange(of: appData, initial: true) {
            Task.detached {
                try await appData.refresh()
            }
        }
        // Legacy updating mechanism
        .task {
            Task.detached {
                repeat {
                    try Task.checkCancellation()
                    if case .ticker(let string) = provider {
                        if !string.isEmpty {
                            print("willUpdate: " + string)
                            print("baseURL: " + (await baseURL.absoluteString))
                            let value = try await String(contentsOf: baseURL.appending(path: "stocks", directoryHint: .isDirectory).appending(path: string, directoryHint: .notDirectory))
                            print("didUpdate: " + string + " value: " + value)
                            await MainActor.run {
                                self.value = Float(value)
                            }
                        }
                        try await Task.sleep(for: .seconds(self.value == nil ? 1 : 60))
                    }
                } while true
            }
        }
    }
}
