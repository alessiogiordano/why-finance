import SwiftUI

struct WidgetView: View {
    let ticker: String
    @State var value: Float?
    @Environment(\.whyFinanceBaseURL) var baseURL
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text(ticker).font(.headline)
            Spacer().frame(maxWidth: .infinity)
            if let value {
                Text(String(format: "%.3f", value)).font(.largeTitle)
                    .minimumScaleFactor(0.1)
            } else {
                Text("---.--").font(.largeTitle)
                    .redacted(reason: .placeholder)
            }
        }.foregroundStyle(.ultraThickMaterial)
            .task {
                Task.detached {
                    repeat {
                        try Task.checkCancellation()
                        if !ticker.isEmpty {
                            print("willUpdate: " + ticker)
                            print("baseURL: " + (await baseURL.absoluteString))
                            let value = try await String(contentsOf: baseURL.appending(path: "watch", directoryHint: .isDirectory).appending(path: ticker, directoryHint: .notDirectory))
                            print("didUpdate: " + ticker + " value: " + value)
                            await MainActor.run {
                                self.value = Float(value)
                            }
                        }
                        try await Task.sleep(for: .seconds(self.value == nil ? 1 : 60))
                    } while true
                }
            }
    }
}
