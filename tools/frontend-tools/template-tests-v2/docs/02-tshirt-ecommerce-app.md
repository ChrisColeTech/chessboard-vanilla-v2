# 02 - T-Shirt Ecommerce App MVP

## Implementation Plan

### Phase 1: Base Application Setup
This app uses the shared base React Vite application with all required dependencies:

1. **Base App Foundation** from `/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/base-app`
   - Vanilla React + Vite + TypeScript
   - Tailwind CSS 3.x
   - HeadlessUI components
   - Lucide React icons
   - React Icons library

2. **T-Shirt App Setup** - Copy base app structure (excluding src) to create tshirt-app directory

3. **Page Generation** - Use template-based generator to create complete t-shirt ecommerce structure

### Phase 2: T-Shirt App Generation
Use the template-based generator to create the complete t-shirt ecommerce app structure on top of the base app foundation.

## App Vision
A sleek online t-shirt store focusing on custom designs, trendy graphics, and street wear. Think "Supreme meets Etsy" with high-quality product photos, size guides, and easy customization options.

## What Makes This Special
- **Design previews** - See shirts on different colored blanks
- **Size visualization** - Interactive size charts and fit guides  
- **Custom text** - Add personalized text to designs
- **Trend tracking** - Popular designs and bestsellers

## Parent Pages & Children

### 1. **Shop** Parent
**Purpose**: Browse t-shirt collections and designs

#### **Trending** Child Page
- **Hero Banner**: Featured trending design of the week
- **Bestsellers Grid**:
  - Top 20 selling designs
  - Sales numbers and trending indicators
  - Quick view on hover
  - Add to cart and wishlist buttons
- **New Arrivals Section**:
  - Latest designs added this week
  - "New" badges on product cards
  - Release date stamps
- **Product Cards Include**:
  - High-res design preview
  - Design name and artist
  - Price range (varies by shirt color/type)
  - Color options preview (small circles)
  - Size availability indicator
  - Heart icon for wishlist
  - Quick add to cart button
- **Sort Options**:
  - Popularity, newest, price low-to-high, price high-to-low
  - Filter by price range
- **Design Detail Modal**:
  - Large design preview
  - Multiple shirt color options
  - Size selector with availability
  - Quantity selector
  - Artist information
  - Design story/inspiration

#### **Categories** Child Page
- **Category Grid**: Visual category tiles
  - Graphic Tees, Vintage, Sports, Funny, Minimalist, Band Tees
  - Representative design previews
  - Item count per category
- **Category Detail View**:
  - Filtered product grid for selected category
  - Category-specific filters (team, decade, humor type)
  - Featured designs in category
- **Style Filters**:
  - Shirt type (crew neck, v-neck, long sleeve)
  - Fit (regular, slim, oversized)
  - Fabric (cotton, blend, organic)
- **Brand Filters**:
  - Independent artists
  - Popular brands
  - Exclusive designs
- **Search Within Category**:
  - Text search for specific themes
  - Tag-based filtering

### 2. **Design** Parent
**Purpose**: Customize and create personalized shirts

#### **Templates** Child Page
- **Template Categories**:
  - Text-based, logo templates, photo frames
  - Holiday themes, sports, motivational
- **Template Grid**:
  - Thumbnail previews of customizable templates
  - Complexity indicators (beginner, intermediate, advanced)
  - Customization options preview
- **Template Editor**:
  - Live preview on shirt mockup
  - Text editing tools (font, size, color, effects)
  - Element repositioning with drag-and-drop
  - Color scheme selector
  - Undo/redo functionality
- **Shirt Customization**:
  - Shirt color selection (20+ colors)
  - Shirt type selection (tee, tank, long sleeve)
  - Size preview and fit guide
- **Save and Share**:
  - Save design to account
  - Share design link
  - Add to cart with custom options

#### **Custom** Child Page
- **Design Upload**:
  - Drag and drop image upload
  - File format guidelines (PNG, JPG, SVG)
  - Resolution requirements
  - Copyright notice and guidelines
- **Text Editor**:
  - Add custom text with rich formatting
  - Font library (50+ fonts)
  - Text effects (shadow, outline, gradient)
  - Multiple text elements support
- **Design Canvas**:
  - Interactive design area
  - Grid and alignment guides
  - Zoom in/out functionality
  - Element layering controls
- **Shirt Preview**:
  - Real-time preview on different shirt colors
  - Front and back design options
  - Size mockup visualization
- **Quality Check**:
  - Print quality indicator
  - Resolution warnings
  - Color accuracy preview

### 3. **Cart** Parent
**Purpose**: Review order and purchase

#### **Review** Child Page
- **Cart Items List**: Each item displays:
  - Product thumbnail with design preview
  - Design name and customizations
  - Shirt color and type
  - Size selection
  - Quantity with +/- controls
  - Individual price
  - Remove item button
- **Customization Summary**:
  - Custom text/uploaded designs
  - Edit design button
  - Preview on shirt mockup
- **Order Summary Panel**:
  - Subtotal calculation
  - Estimated shipping cost
  - Tax calculation (based on location)
  - Discount codes section
  - Total amount (prominent)
- **Shipping Calculator**:
  - ZIP code input for estimates
  - Shipping speed options
  - Delivery date estimates
- **Continue Shopping Button**
- **Proceed to Checkout Button**

#### **Checkout** Child Page
- **Shipping Information**:
  - Address form with autocomplete
  - Saved addresses for returning customers
  - Address validation
- **Shipping Options**:
  - Standard (5-7 days)
  - Expedited (2-3 days)
  - Overnight shipping
  - Price and delivery date for each option
- **Payment Section**:
  - Credit card form
  - PayPal integration
  - Apple Pay/Google Pay options
  - Saved payment methods
- **Order Review**:
  - Mini cart summary
  - Final price breakdown
  - Estimated delivery date
- **Promo Codes**:
  - Code input field
  - Applied discounts display
- **Place Order Button**
- **Order Confirmation**:
  - Order number generation
  - Email confirmation
  - Tracking information setup

### 4. **Account** Parent
**Purpose**: User profile and order management

#### **Orders** Child Page
- **Order History List**: Each order shows:
  - Order number and date
  - Order status (Processing, Shipped, Delivered)
  - Total amount and item count
  - Thumbnail images of ordered designs
  - Tracking button (if shipped)
  - Reorder button
  - Leave review button (if delivered)
- **Order Detail View**:
  - Complete item list with customizations
  - Shipping address used
  - Payment method
  - Order timeline and status updates
  - Tracking information
  - Return/exchange options
- **Order Status Tracking**:
  - Progress indicator
  - Estimated delivery updates
  - Shipping carrier information
- **Returns & Exchanges**:
  - Return request form
  - Return policy information
  - Exchange size/color options
- **Order Filters**:
  - Date range selection
  - Order status filter
  - Amount range filter

#### **Wishlist** Child Page
- **Saved Designs Grid**:
  - All hearted/saved designs
  - Design previews on shirts
  - Save date stamps
  - Quick add to cart buttons
- **Wishlist Organization**:
  - Create custom collections
  - Tag designs (gifts, personal, work)
  - Sort by date added, price, popularity
- **Share Wishlist**:
  - Generate shareable wishlist link
  - Social media sharing options
  - Gift suggestion features
- **Price Tracking**:
  - Sale alerts for wishlisted items
  - Price drop notifications
  - Limited time offer alerts
- **Quick Actions**:
  - Move to cart
  - Remove from wishlist
  - Share individual design
- **Design Collections**:
  - Group related designs
  - Themed collections (summer, work, gifts)
  - Collection sharing options

## Theme & Layout System

### Crimson Theme
This app uses the **Crimson** theme from the professional themes collection, providing a bold, fashion-forward aesthetic perfect for t-shirt retail.

**Theme Variables (Crimson):**
```css
/* Crimson Theme Variables */
--primary: #dc2626;           /* Crimson red primary */
--accent: #dc2626;            /* Crimson red accent */
--background: #0f172a;        /* Slate dark background */
--surface: #1e293b;           /* Slate surface */
--surface-variant: #334155;   /* Slate surface variant */
--on-surface: #f1f5f9;        /* Slate light text */
--on-surface-variant: #cbd5e1; /* Slate medium text */
--outline: #475569;           /* Slate outline */
```

### App Layout & Navigation
The app uses `AppLayout.tsx` with TabBar navigation:

**Tab Configuration:**
- **Shop** - Store icon (Trending, Categories)
- **Design** - Palette icon (Templates, Custom)
- **Cart** - Shopping cart icon (Review, Checkout)
- **Account** - User icon (Orders, Wishlist)

### Layout Templates

#### Desktop Pages (ChessboardLayout)
5-panel design for comprehensive product browsing:
```jsx
<ChessboardLayout
  topLeft={<div className="tshirt-filters">Filters/Sort</div>}
  top={<div className="tshirt-search">Search/Navigation</div>}
  topRight={<div className="tshirt-cart-info">Cart/User Info</div>}
  left={<div className="tshirt-categories">Categories/Size Guide</div>}
  center={<div className="tshirt-products">Product Grid/Editor</div>}
  right={<div className="tshirt-details">Product/Design Details</div>}
  bottomLeft={<div className="tshirt-tools">Design Tools</div>}
  bottom={<div className="tshirt-status">Progress/Status</div>}
  bottomRight={<div className="tshirt-actions">Quick Actions</div>}
/>
```

#### Mobile Pages (MobileChessboardLayout)
3-panel design optimized for mobile shopping:
```jsx
<MobileChessboardLayout
  topPieces={<div className="tshirt-mobile-header">Search/Cart</div>}
  center={<div className="tshirt-mobile-content">Product Grid/Editor</div>}
  bottomPieces={<div className="tshirt-mobile-actions">Actions/Tools</div>}
/>
```

### Custom Component Classes

**⚠️ IMPORTANT**: After app generation, add these NEW custom classes to the generated `tshirt-app/src/index.css` file:
- **Use ONLY existing theme variables** (--primary, --accent, --surface, etc.) from professional themes
- **Use standard Tailwind classes** that reference theme variables
- **NO hardcoded colors** - only theme-aware classes
- **Templates are NEVER modified** - only the generated app's CSS

Add these NEW classes to the generated `tshirt-app/src/index.css`:

```css
/* T-Shirt App Component Classes */
.tshirt-product-card {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-lg overflow-hidden;
  @apply hover:bg-surface-variant/60 hover:border-primary/30 transition-all duration-300;
  @apply group cursor-pointer;
}

.tshirt-product-image {
  @apply aspect-square w-full object-cover;
  @apply group-hover:scale-105 transition-transform duration-300;
}

.tshirt-color-selector {
  @apply flex gap-1 flex-wrap;
}

.tshirt-color-option {
  @apply w-6 h-6 rounded-full border-2 border-outline/30 cursor-pointer;
  @apply hover:border-primary/60 transition-colors;
}

.tshirt-size-button {
  @apply px-3 py-1 border border-outline/30 rounded-md text-sm;
  @apply hover:border-primary/60 hover:bg-primary/10 transition-all;
  @apply data-[selected=true]:border-primary data-[selected=true]:bg-primary/20;
}

.tshirt-design-canvas {
  @apply bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-lg;
  @apply relative overflow-hidden min-h-96;
}

.tshirt-cart-item {
  @apply flex gap-4 p-4 bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-lg;
  @apply hover:bg-surface-variant/40 transition-colors;
}

.tshirt-price-tag {
  @apply text-primary font-semibold text-lg;
}

.tshirt-category-card {
  @apply bg-gradient-to-br from-primary/20 to-accent/10;
  @apply border border-primary/30 rounded-xl p-6 text-center;
  @apply hover:from-primary/30 hover:to-accent/20 transition-all duration-300;
  @apply cursor-pointer;
}

.tshirt-wishlist-button {
  @apply p-2 rounded-full bg-surface/80 backdrop-blur-sm;
  @apply hover:bg-primary/20 hover:text-primary transition-all;
  @apply data-[wishlisted=true]:bg-primary/20 data-[wishlisted=true]:text-primary;
}
```

### ASCII Mockups

#### Desktop Layout (ChessboardLayout)
```
┌─────────────────────────────────────────────────────────────────┐
│                     T-Shirt Ecommerce App                      │
├─────────┬─────────────────────────┬─────────────────────────────┤
│Filters/ │    Search/Navigation    │    Cart/User Info           │
│ Sort    │                         │                             │
├─────────┼─────────────────────────┼─────────────────────────────┤
│         │                         │                             │
│Category │                         │  Product/Design Details     │
│Size     │   Product Grid/Editor   │                             │
│Guide    │                         │                             │
│         │                         │                             │
├─────────┼─────────────────────────┼─────────────────────────────┤
│ Design  │   Progress/Status       │    Quick Actions            │
│ Tools   │                         │                             │
├─────────┴─────────────────────────┴─────────────────────────────┤
│                          TabBar                                 │
│      Shop      Design      Cart      Account                    │
└─────────────────────────────────────────────────────────────────┘
```

#### Mobile Layout (MobileChessboardLayout)
```
┌─────────────────────────────────┐
│       T-Shirt Ecommerce App     │
├─────────────────────────────────┤
│        Search/Cart              │
│                                 │
├─────────────────────────────────┤
│                                 │
│                                 │
│     Product Grid/Editor         │
│                                 │
│                                 │
├─────────────────────────────────┤
│       Actions/Tools             │
│                                 │
├─────────────────────────────────┤
│             TabBar              │
│   Shop   Design   Cart  Account │
└─────────────────────────────────┘
```

## Key Features
- High-res product photos with zoom
- Color selector with live preview
- Size chart modal with measurements
- Custom text editor with font options
- Shopping cart with size/color summary
- Wishlist heart buttons
- Order tracking simulation
- Design upload functionality

## Technical Implementation
- Product image swapping for different colors
- Canvas API for custom text rendering
- Local storage for cart and wishlist
- Mock payment processing
- Responsive product grid layouts
- Image zoom functionality
- Size guide overlay modals

## Demo Highlights
- Browse trendy t-shirt designs with smooth filtering
- Customize shirts with text and color changes
- Interactive size chart and fit guide
- Shopping cart with live total calculations
- Clean checkout flow with shipping options
- Mobile-optimized product browsing

## Mobile Page Variants

Each child page has a corresponding mobile version optimized for touch and smaller screens:

#### **Mobile Trending Page**
- **Vertical Product Grid**: Single column layout for trending designs
- **Swipe Gallery**: Horizontal swipe through product images
- **Touch Sort**: Large sort buttons and filter toggles
- **Quick Actions**: Swipe to add to cart or wishlist
- **Mobile Modals**: Full-screen design detail modals

#### **Mobile Categories Page**
- **Category Cards**: Full-width category tiles for easy tapping
- **Filter Slides**: Slide-out filter panels optimized for mobile
- **Touch Navigation**: Gesture-based category browsing
- **Mobile Grid**: Responsive product grid for mobile viewing

#### **Mobile Templates Page**
- **Template Carousel**: Swipeable template previews
- **Touch Editor**: Mobile-optimized design editor with touch controls
- **Mobile Canvas**: Pinch-to-zoom design canvas
- **Quick Save**: One-tap save and share functionality

#### **Mobile Custom Page**
- **Upload Flow**: Mobile camera integration for image uploads
- **Touch Text Editor**: Mobile keyboard optimized text editing
- **Preview Gestures**: Pinch and zoom for design preview
- **Mobile Tools**: Touch-friendly design tools and controls

#### **Mobile Cart Review Page**
- **Vertical Item List**: Single column cart items layout
- **Swipe Actions**: Swipe to remove or edit cart items
- **Sticky Summary**: Fixed order summary at bottom
- **Mobile Checkout**: Touch-optimized checkout flow

#### **Mobile Cart Checkout Page**
- **Step Progress**: Mobile progress indicator
- **Form Optimization**: Mobile keyboard friendly forms
- **Payment Quick**: Apple Pay/Google Pay integration
- **Address Auto**: Mobile location and autocomplete

#### **Mobile Orders Page**
- **Order Cards**: Mobile-optimized order history cards
- **Touch Tracking**: Tap to expand order tracking details
- **Swipe Actions**: Swipe to reorder or view details
- **Mobile Timeline**: Touch-friendly order status timeline

#### **Mobile Wishlist Page**
- **Grid Layout**: Mobile-optimized wishlist grid
- **Quick Actions**: One-tap move to cart or remove
- **Share Options**: Mobile sharing for wishlist items
- **Touch Management**: Gesture-based wishlist organization

## Implementation Commands

### Phase 1: Setup T-Shirt App Directory

```bash
# Copy base app structure (excluding src folder) to tshirt-app
cd /mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2
mkdir -p tshirt-app
cp -r base-app/{package.json,package-lock.json,vite.config.ts,tsconfig.json,tsconfig.node.json,tailwind.config.js,postcss.config.js,index.html,public} tshirt-app/

# Navigate to tshirt app directory and install dependencies
cd tshirt-app
npm install
cd ..
```

### Phase 2: Generate T-Shirt App Pages

```bash
# Navigate to generator directory
cd tshirt-app

# Create parent pages
npm run mobile -- parent Shop
npm run mobile -- parent Design
npm run mobile -- parent Cart
npm run mobile -- parent Account

# Create child pages with mobile variants under Shop parent
npm run mobile -- child Trending --parent shop npm run mobile -- child Categories --parent shop 
# Create child pages with mobile variants under Design parent
npm run mobile -- child Templates --parent design npm run mobile -- child Custom --parent design 
# Create child pages with mobile variants under Cart parent
npm run mobile -- child Review --parent cart npm run mobile -- child Checkout --parent cart 
# Create child pages with mobile variants under Account parent
npm run mobile -- child Orders --parent account npm run mobile -- child Wishlist --parent account ```

## File Structure Tree

```
tshirt-app/
├── src/
│   ├── components/
│   │   ├── shop/
│   │   │   ├── TrendingPageWrapper.tsx
│   │   │   ├── CategoriesPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── design/
│   │   │   ├── TemplatesPageWrapper.tsx
│   │   │   ├── CustomPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── cart/
│   │   │   ├── ReviewPageWrapper.tsx
│   │   │   ├── CheckoutPageWrapper.tsx
│   │   │   └── index.ts
│   │   └── account/
│   │       ├── OrdersPageWrapper.tsx
│   │       ├── WishlistPageWrapper.tsx
│   │       └── index.ts
│   ├── pages/
│   │   ├── shop/
│   │   │   ├── ShopPage.tsx
│   │   │   ├── ShopMainPage.tsx
│   │   │   ├── TrendingPage.tsx
│   │   │   ├── MobileTrendingPage.tsx
│   │   │   ├── CategoriesPage.tsx
│   │   │   └── MobileCategoriesPage.tsx
│   │   ├── design/
│   │   │   ├── DesignPage.tsx
│   │   │   ├── DesignMainPage.tsx
│   │   │   ├── TemplatesPage.tsx
│   │   │   ├── MobileTemplatesPage.tsx
│   │   │   ├── CustomPage.tsx
│   │   │   └── MobileCustomPage.tsx
│   │   ├── cart/
│   │   │   ├── CartPage.tsx
│   │   │   ├── CartMainPage.tsx
│   │   │   ├── ReviewPage.tsx
│   │   │   ├── MobileReviewPage.tsx
│   │   │   ├── CheckoutPage.tsx
│   │   │   └── MobileCheckoutPage.tsx
│   │   └── account/
│   │       ├── AccountPage.tsx
│   │       ├── AccountMainPage.tsx
│   │       ├── OrdersPage.tsx
│   │       ├── MobileOrdersPage.tsx
│   │       ├── WishlistPage.tsx
│   │       └── MobileWishlistPage.tsx
│   ├── hooks/
│   │   ├── shop/
│   │   │   └── useShopActions.ts
│   │   ├── design/
│   │   │   └── useDesignActions.ts
│   │   ├── cart/
│   │   │   └── useCartActions.ts
│   │   └── account/
│   │       └── useAccountActions.ts
│   ├── services/
│   │   ├── api/
│   │   │   ├── productsApi.ts
│   │   │   ├── designsApi.ts
│   │   │   ├── cartApi.ts
│   │   │   └── ordersApi.ts
│   │   └── instructions/
│   │       └── pages/
│   │           ├── shop.ts
│   │           ├── design.ts
│   │           ├── cart.ts
│   │           └── account.ts
│   ├── constants/
│   │   └── actions/
│   │       └── pages/
│   │           ├── shop.ts
│   │           ├── design.ts
│   │           ├── cart.ts
│   │           └── account.ts
│   └── types/
│       ├── products.ts
│       ├── designs.ts
│       ├── cart.ts
│       └── orders.ts
```

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL, -- graphic-tees, vintage, sports, funny
    description TEXT,
    image_url VARCHAR(500),
    active BOOLEAN DEFAULT TRUE
);

-- Artists/Designers table
CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    profile_image_url VARCHAR(500),
    social_links JSONB, -- Instagram, Twitter, etc.
    commission_rate DECIMAL(5,2) DEFAULT 15.00, -- percentage
    created_at TIMESTAMP DEFAULT NOW()
);

-- Designs table
CREATE TABLE designs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    artist_id INTEGER REFERENCES artists(id),
    category_id INTEGER REFERENCES categories(id),
    design_file_url VARCHAR(500) NOT NULL, -- high-res design file
    preview_url VARCHAR(500), -- design preview image
    tags TEXT[], -- funny, vintage, music, etc.
    price_base DECIMAL(10,2) NOT NULL, -- base price before shirt cost
    is_customizable BOOLEAN DEFAULT FALSE,
    popularity_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Shirt types and options
CREATE TABLE shirt_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL, -- crew-neck, v-neck, tank, long-sleeve
    material VARCHAR(100), -- cotton, blend, organic
    fit VARCHAR(50), -- regular, slim, oversized
    base_price DECIMAL(10,2) NOT NULL,
    available_sizes TEXT[] DEFAULT ARRAY['XS','S','M','L','XL','XXL'],
    available_colors TEXT[] DEFAULT ARRAY['white','black','gray','navy'],
    active BOOLEAN DEFAULT TRUE
);

-- Products (design + shirt type combinations)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    design_id INTEGER REFERENCES designs(id),
    shirt_type_id INTEGER REFERENCES shirt_types(id),
    color VARCHAR(50) NOT NULL,
    size VARCHAR(10) NOT NULL,
    final_price DECIMAL(10,2) NOT NULL, -- design price + shirt price
    stock_quantity INTEGER DEFAULT 0,
    sku VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Custom designs (user created)
CREATE TABLE custom_designs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255),
    design_data JSONB NOT NULL, -- custom text, uploaded images, etc.
    preview_url VARCHAR(500),
    shirt_type_id INTEGER REFERENCES shirt_types(id),
    color VARCHAR(50),
    size VARCHAR(10),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Shopping cart
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id), -- for pre-made designs
    custom_design_id INTEGER REFERENCES custom_designs(id), -- for custom designs
    quantity INTEGER DEFAULT 1,
    added_at TIMESTAMP DEFAULT NOW(),
    CHECK ((product_id IS NOT NULL AND custom_design_id IS NULL) OR 
           (product_id IS NULL AND custom_design_id IS NOT NULL))
);

-- Orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, shipped, delivered
    subtotal DECIMAL(10,2) NOT NULL,
    shipping_cost DECIMAL(10,2) DEFAULT 0,
    tax DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    shipping_address JSONB NOT NULL,
    tracking_number VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP
);

-- Order items
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    custom_design_id INTEGER REFERENCES custom_designs(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    CHECK ((product_id IS NOT NULL AND custom_design_id IS NULL) OR 
           (product_id IS NULL AND custom_design_id IS NOT NULL))
);

-- Wishlist
CREATE TABLE wishlist_items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    design_id INTEGER REFERENCES designs(id),
    shirt_type_id INTEGER REFERENCES shirt_types(id),
    preferred_color VARCHAR(50),
    preferred_size VARCHAR(10),
    added_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, design_id, shirt_type_id)
);

-- Design templates (for customization)
CREATE TABLE design_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100), -- text-based, logo, photo-frame
    template_data JSONB NOT NULL, -- template structure
    preview_url VARCHAR(500),
    complexity_level VARCHAR(20) DEFAULT 'beginner', -- beginner, intermediate, advanced
    price_modifier DECIMAL(5,2) DEFAULT 0.00, -- additional cost for template
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## API Routes

### Authentication Routes
```
POST   /api/auth/register        # User registration
POST   /api/auth/login           # User login
POST   /api/auth/logout          # User logout
```

### Product Routes (Shop Pages)
```
GET    /api/products             # Get all products with filters
GET    /api/products/trending    # Get trending/bestselling designs
GET    /api/products/categories  # Get product categories
GET    /api/products/category/:id # Get products by category
GET    /api/products/:id         # Get specific product details
GET    /api/designs              # Get all designs
GET    /api/designs/:id          # Get design details
GET    /api/shirt-types          # Get available shirt types and options
```

### Design Routes (Design Pages)
```
GET    /api/design/templates     # Get design templates
GET    /api/design/templates/:id # Get specific template
POST   /api/design/custom        # Save custom design
PUT    /api/design/custom/:id    # Update custom design
DELETE /api/design/custom/:id    # Delete custom design
GET    /api/design/user-designs  # Get user's custom designs
POST   /api/design/upload        # Upload custom image for design
```

### Cart Routes (Cart Pages)
```
GET    /api/cart                 # Get user's cart items
POST   /api/cart/add             # Add item to cart
PUT    /api/cart/update/:id      # Update cart item
DELETE /api/cart/remove/:id      # Remove item from cart
DELETE /api/cart/clear           # Clear entire cart
POST   /api/cart/checkout        # Process checkout
```

### Order Routes (Account Pages)
```
GET    /api/orders               # Get user's order history
GET    /api/orders/:id           # Get specific order details
GET    /api/orders/:id/tracking  # Get order tracking information
POST   /api/orders/:id/reorder   # Reorder previous order
```

### Wishlist Routes (Account Pages)
```
GET    /api/wishlist             # Get user's wishlist
POST   /api/wishlist/add         # Add item to wishlist
DELETE /api/wishlist/remove/:id  # Remove item from wishlist
PUT    /api/wishlist/update/:id  # Update wishlist item preferences
```

### Artist Routes
```
GET    /api/artists              # Get all artists/designers
GET    /api/artists/:id          # Get artist details
GET    /api/artists/:id/designs  # Get designs by artist
```

### User Routes
```
GET    /api/user/profile         # Get user profile
PUT    /api/user/profile         # Update user profile
GET    /api/user/addresses       # Get user addresses
POST   /api/user/addresses       # Add new address
PUT    /api/user/addresses/:id   # Update address
DELETE /api/user/addresses/:id   # Delete address
```

### Size and Fit Routes
```
GET    /api/sizing/chart         # Get size chart information
GET    /api/sizing/guide/:type   # Get fit guide for shirt type
```