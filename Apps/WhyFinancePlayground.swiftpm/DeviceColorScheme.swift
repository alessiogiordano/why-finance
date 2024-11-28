import SwiftUI

struct DeviceColorSchemeKey: EnvironmentKey {
    static let defaultValue = ColorScheme.light
}

extension EnvironmentValues {
    var deviceColorScheme: ColorScheme {
        get { self[DeviceColorSchemeKey.self] }
        set { self[DeviceColorSchemeKey.self] = newValue }
    }
}
