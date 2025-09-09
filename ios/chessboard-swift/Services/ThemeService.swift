// ThemeService.swift - Comprehensive theme management
import SwiftUI

@MainActor
class ThemeService: ObservableObject {
    @Published var currentTheme: ThemeID = .dark
    @Published var selectedBaseTheme: BaseThemeID = .default
    @Published var isDarkMode: Bool = true
    
    private let themes: [ThemeID: any ChessTheme]
    
    init() {
        // Initialize available themes
        self.themes = [
            .dark: DefaultDarkTheme(),
            .light: DefaultLightTheme(),
            .cyberNeon: CyberNeonDarkTheme(),
            .cyberNeonLight: CyberNeonLightTheme(),
            .dragonGold: DragonGoldDarkTheme(),
            .dragonGoldLight: DragonGoldLightTheme(),
            .shadowKnight: ShadowKnightDarkTheme(),
            .shadowKnightLight: ShadowKnightLightTheme(),
            .forestMystique: ForestMystiqueDarkTheme(),
            .forestMystiqueLight: ForestMystiqueLightTheme(),
            .royalPurple: RoyalPurpleDarkTheme(),
            .royalPurpleLight: RoyalPurpleLightTheme()
        ]
        
        loadPersistedTheme()
    }
    
    var current: any ChessTheme {
        return themes[currentTheme] ?? DefaultDarkTheme()
    }
    
    func applyTheme(_ themeID: ThemeID) {
        currentTheme = themeID
        selectedBaseTheme = themeID.baseTheme
        isDarkMode = !themeID.isLight
        
        updateSystemAppearance()
        saveTheme(themeID)
        
        print("🎨 Applied theme: \(current.name)")
    }
    
    func setBaseTheme(_ baseTheme: BaseThemeID) {
        selectedBaseTheme = baseTheme
        
        let newThemeID: ThemeID = {
            switch baseTheme {
            case .default:
                return isDarkMode ? .dark : .light
            case .cyberNeon:
                return isDarkMode ? .cyberNeon : .cyberNeonLight
            case .dragonGold:
                return isDarkMode ? .dragonGold : .dragonGoldLight
            case .shadowKnight:
                return isDarkMode ? .shadowKnight : .shadowKnightLight
            case .forestMystique:
                return isDarkMode ? .forestMystique : .forestMystiqueLight
            case .royalPurple:
                return isDarkMode ? .royalPurple : .royalPurpleLight
            }
        }()
        
        applyTheme(newThemeID)
    }
    
    func toggleMode() {
        isDarkMode.toggle()
        
        let newThemeID: ThemeID = {
            switch selectedBaseTheme {
            case .default:
                return isDarkMode ? .dark : .light
            case .cyberNeon:
                return isDarkMode ? .cyberNeon : .cyberNeonLight
            case .dragonGold:
                return isDarkMode ? .dragonGold : .dragonGoldLight
            case .shadowKnight:
                return isDarkMode ? .shadowKnight : .shadowKnightLight
            case .forestMystique:
                return isDarkMode ? .forestMystique : .forestMystiqueLight
            case .royalPurple:
                return isDarkMode ? .royalPurple : .royalPurpleLight
            }
        }()
        
        applyTheme(newThemeID)
    }
    
    func getAvailableBaseThemes() -> [BaseThemeConfig] {
        return [
            BaseThemeConfig(
                id: .default,
                name: "Default",
                description: "Classic clean theme",
                icon: "paintbrush.fill",
                darkTheme: themes[.dark]!,
                lightTheme: themes[.light]!
            ),
            BaseThemeConfig(
                id: .cyberNeon,
                name: "Cyber Neon",
                description: "Electric neon gaming",
                icon: "bolt.fill",
                darkTheme: themes[.cyberNeon]!,
                lightTheme: themes[.cyberNeonLight]!
            ),
            BaseThemeConfig(
                id: .dragonGold,
                name: "Dragon Gold",
                description: "Medieval dragon power",
                icon: "crown.fill",
                darkTheme: themes[.dragonGold]!,
                lightTheme: themes[.dragonGoldLight]!
            ),
            BaseThemeConfig(
                id: .shadowKnight,
                name: "Shadow Knight",
                description: "Dark steel armor",
                icon: "shield.fill",
                darkTheme: themes[.shadowKnight]!,
                lightTheme: themes[.shadowKnightLight]!
            ),
            BaseThemeConfig(
                id: .forestMystique,
                name: "Forest Mystique",
                description: "Mystic nature theme",
                icon: "tree.fill",
                darkTheme: themes[.forestMystique]!,
                lightTheme: themes[.forestMystiqueLight]!
            ),
            BaseThemeConfig(
                id: .royalPurple,
                name: "Royal Purple",
                description: "Majestic royal theme",
                icon: "gem.fill",
                darkTheme: themes[.royalPurple]!,
                lightTheme: themes[.royalPurpleLight]!
            )
        ]
    }
    
    private func loadPersistedTheme() {
        // For now, use default theme
        // In full implementation, would load from UserDefaults
    }
    
    private func saveTheme(_ themeID: ThemeID) {
        // For now, just log
        // In full implementation, would save to UserDefaults
        print("💾 Saving theme: \(themeID.rawValue)")
    }
    
    private func updateSystemAppearance() {
        #if os(iOS)
        DispatchQueue.main.async {
            // This would update system appearance in full implementation
            print("🎨 Updating system appearance to: \(self.isDarkMode ? "dark" : "light")")
        }
        #endif
    }
}

struct BaseThemeConfig: Identifiable {
    let id: BaseThemeID
    let name: String
    let description: String
    let icon: String
    let darkTheme: any ChessTheme
    let lightTheme: any ChessTheme
    
    func theme(isDark: Bool) -> any ChessTheme {
        return isDark ? darkTheme : lightTheme
    }
}