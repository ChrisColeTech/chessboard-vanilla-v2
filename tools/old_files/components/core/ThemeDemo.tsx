import { BackgroundEffects } from '../layout/BackgroundEffects'
import { ThemeSwitcher } from './ThemeSwitcher'

export function ThemeDemo() {
  return (
    <div className="min-h-screen bg-background transition-all duration-500 relative">
      {/* Background Effects */}
      <BackgroundEffects />
      
      {/* Main Content */}
      <div className="relative z-10 flex items-center justify-center min-h-screen p-4">
        <div className="w-full max-w-4xl mx-auto space-y-8">
          {/* Header Section */}
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-6xl font-bold text-primary-gradient animate-card-entrance">
              Chess Training
            </h1>
            <p className="text-xl text-muted-foreground animate-card-entrance animation-delay-200">
              Gaming Themes Showcase
            </p>
          </div>
          
          {/* Theme Switcher */}
          <div className="flex justify-center animate-card-entrance animation-delay-500">
            <div className="bg-card/20 backdrop-blur-xl border border-border/20 rounded-xl p-6 shadow-gaming">
              <h3 className="text-lg font-semibold text-foreground mb-4 text-center">
                Select Theme
              </h3>
              <ThemeSwitcher onOpenSettings={() => {}} />
            </div>
          </div>
          
          {/* Demo Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-card-entrance animation-delay-1000">
            {/* Primary Button Card */}
            <div className="card-gaming p-6 space-y-4">
              <h3 className="text-lg font-semibold text-foreground">Primary Actions</h3>
              <button className="btn-gaming-primary gpu-accelerated">
                Play Game
              </button>
              <button className="btn-gaming-secondary gpu-accelerated">
                View Stats
              </button>
            </div>
            
            {/* Form Elements Card */}
            <div className="card-gaming p-6 space-y-4">
              <h3 className="text-lg font-semibold text-foreground">Form Elements</h3>
              <input 
                type="text" 
                placeholder="Username"
                className="input-gaming w-full py-2 px-3"
              />
              <input 
                type="email" 
                placeholder="Email"
                className="input-gaming w-full py-2 px-3"
              />
            </div>
            
            {/* Text Styles Card */}
            <div className="card-gaming p-6 space-y-4">
              <h3 className="text-lg font-semibold text-foreground">Typography</h3>
              <p className="text-gaming-gradient font-bold text-lg">
                Gradient Text
              </p>
              <p className="text-foreground">
                Primary text content
              </p>
              <p className="text-muted-foreground text-sm">
                Muted text content
              </p>
            </div>
            
            {/* Interactive Elements */}
            <div className="card-gaming p-6 space-y-4">
              <h3 className="text-lg font-semibold text-foreground">Interactive</h3>
              <div className="space-y-2">
                <div className="bg-primary/20 border border-primary/30 rounded-lg p-3 hover-grow cursor-pointer transition-all">
                  <p className="text-primary font-medium">Hover Effect</p>
                </div>
                <div className="bg-accent/20 border border-accent/30 rounded-lg p-3 hover-glow cursor-pointer">
                  <p className="text-accent font-medium">Glow Effect</p>
                </div>
              </div>
            </div>
            
            {/* Shadows and Effects */}
            <div className="card-gaming p-6 space-y-4">
              <h3 className="text-lg font-semibold text-foreground">Effects</h3>
              <div className="bg-primary/10 border border-primary/20 rounded-lg p-4 shadow-primary">
                <p className="text-primary text-sm">Primary Shadow</p>
              </div>
              <div className="bg-accent/10 border border-accent/20 rounded-lg p-4 shadow-accent">
                <p className="text-accent text-sm">Accent Shadow</p>
              </div>
            </div>
            
            {/* Gaming Aesthetics */}
            <div className="card-gaming p-6 space-y-4">
              <h3 className="text-lg font-semibold text-foreground">Gaming UI</h3>
              <div className="glass rounded-lg p-4 glass-hover">
                <p className="text-foreground font-medium">Glass Morphism</p>
                <p className="text-muted-foreground text-sm">Backdrop blur effect</p>
              </div>
            </div>
          </div>
          
          {/* Footer */}
          <div className="text-center text-muted-foreground text-sm animate-card-entrance animation-delay-2000">
            <p>Modern gaming themes with light and dark variants</p>
            <p className="mt-2">Following the Chess Training App Style Guide</p>
          </div>
        </div>
      </div>
    </div>
  )
}