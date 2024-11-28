import SwiftUI

extension View {
    func systemSmallWidget(background: LinearGradient? = LinearGradient(colors: [.pink, .purple], startPoint: .top, endPoint: .bottom)) -> some View {
        self.modifier(SystemSmallWidget(background: background))
    }
}

extension LinearGradient {
    init(colors: [Color]) {
        self.init(colors: colors, startPoint: .top, endPoint: .bottom)
    }
}

struct SystemSmallWidget: ViewModifier {
    let background: LinearGradient?
    
    init(background: LinearGradient? = LinearGradient(colors: [.pink, .purple], startPoint: .top, endPoint: .bottom)) {
        self.background = background
    }
    
    func body(content: Content) -> some View {
        VStack {
            content.padding()
        }
        .frame(width: 170, height: 170)
        .background {
            background ?? LinearGradient(colors: [.clear])
        }
        .overlay {
            RoundedRectangle(cornerRadius: 17.0)
                .stroke(Material.thin, lineWidth: 3.0)
        }
        .cornerRadius(17.0)
    }
}
