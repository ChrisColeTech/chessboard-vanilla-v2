# 00 - Cannabis Dispensary/Delivery App MVP

## Implementation Plan

### Phase 1: Base Application Setup
Before creating the cannabis dispensary app, we'll create a base vanilla React Vite application with all required dependencies:

1. **Create Base App Structure** in `/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/base-app`
   - Vanilla React + Vite
   - Tailwind CSS 3.x
   - HeadlessUI components
   - Lucide React icons
   - React Icons library

2. **Test Base App** - Ensure the base application builds successfully with all dependencies

3. **Prepare for App Creation** - Once base app is verified, copy everything except the `src` folder to create individual app directories

### Phase 2: Cannabis App Generation
Use the template-based generator to create the complete cannabis dispensary structure on top of the base app foundation.

## App Vision
A clean, professional cannabis dispensary app focusing on product browsing, ordering, and delivery tracking. Think "Uber Eats for cannabis" with a modern, trustworthy interface that feels legitimate and safe.

## What Makes This Special
- **Age verification flow** - Professional compliance features
- **Delivery tracking** - Real-time order status like food delivery
- **Product education** - Strain info, effects, THC/CBD content
- **Local compliance** - Designed for legal markets only

## Parent Pages & Children

### 1. **Shop** Parent
**Purpose**: Browse and search products

#### **Flower** Child Page
- **Product Grid**: Cards showing strain photos, names, THC/CBD percentages
- **Filter Tabs**: Indica, Sativa, Hybrid, All strains
- **Sort Dropdown**: By price, THC%, popularity, alphabetical
- **Search Bar**: Find strains by name or effects
- **Product Cards Include**: 
  - High-res strain photo
  - Strain name and type
  - THC% and CBD% badges
  - Price per gram/eighth
  - Effects tags (relaxing, energizing, creative)
  - Heart icon to favorite
  - Quick add to cart button
- **Strain Detail Modal**: Opens when card clicked
  - Large strain photo
  - Full effects description
  - Growing info (indoor/outdoor)
  - User reviews and ratings
  - Quantity selector
  - Add to cart button

#### **Edibles** Child Page
- **Category Tabs**: Gummies, Chocolates, Drinks, Baked Goods
- **Dosage Filter**: 2.5mg, 5mg, 10mg, 25mg+ THC
- **Product Grid**: Similar to flower but with different info
- **Product Cards Include**:
  - Product photo
  - Brand and product name
  - THC mg per piece and per package
  - Price and package size
  - Flavor options
  - Onset time (30min, 1hr, 2hr)
  - Add to favorites
  - Quick add to cart
- **Product Detail Modal**:
  - Multiple product photos
  - Ingredients list
  - Dosage guide for beginners
  - Effects timeline
  - Quantity and flavor selector

### 2. **Cart** Parent  
**Purpose**: Review order and checkout

#### **Review** Child Page
- **Cart Items List**: Each item shows:
  - Product photo thumbnail
  - Name and strain/flavor
  - THC/CBD content
  - Quantity selector (+ and - buttons)
  - Individual price
  - Remove item X button
- **Order Summary Card**:
  - Subtotal calculation
  - Delivery fee
  - Tax calculation
  - Total amount (large, bold)
- **Promo Code Section**:
  - Text input for discount codes
  - Apply button
  - Shows discount amount if applied
- **Continue Shopping Button**
- **Proceed to Checkout Button** (disabled if cart empty)

#### **Checkout** Child Page
- **Delivery Address Section**:
  - Saved addresses dropdown
  - Add new address form
  - Address validation
- **Delivery Time Selection**:
  - ASAP option with ETA
  - Scheduled delivery time slots
- **Payment Section**:
  - Credit card form (demo only)
  - Saved payment methods
  - Apple Pay / Google Pay buttons
- **Order Review Summary**:
  - Mini cart with items
  - Total breakdown
- **Legal Disclaimers**:
  - Age verification checkbox
  - Terms acceptance
- **Place Order Button**

### 3. **Orders** Parent
**Purpose**: Track current and past orders

#### **Active** Child Page
- **Current Order Card** (if exists):
  - Order number and status
  - ETA countdown timer
  - Progress tracker: Preparing → Out for Delivery → Delivered
  - Driver info and photo
  - Live map with delivery location
  - Contact driver button
  - Order items summary
- **Empty State** (no active orders):
  - Illustration
  - "No active orders" message
  - "Start Shopping" button
- **Order Status Updates**:
  - Real-time status changes
  - Push notification simulation
  - Estimated delivery time adjustments

#### **History** Child Page
- **Order History List**: Each order shows:
  - Order date and number
  - Order status (Delivered, Cancelled)
  - Total amount
  - Number of items
  - Small thumbnails of products
  - "Reorder" button
  - "View Details" button
- **Order Detail Modal**:
  - Full item list with quantities
  - Delivery address used
  - Payment method
  - Order timeline
  - Receipt download button
- **Filter Options**:
  - Date range picker
  - Order status filter
  - Amount range filter
- **Search**: Find orders by product name

### 4. **Account** Parent
**Purpose**: User profile and preferences

#### **Profile** Child Page
- **User Info Section**:
  - Profile photo upload
  - Name, email, phone editing
  - Age verification status
  - Account creation date
- **Delivery Addresses**:
  - List of saved addresses
  - Add new address button
  - Edit/delete existing addresses
  - Set default address
- **Payment Methods**:
  - Saved credit cards (last 4 digits)
  - Add new payment method
  - Remove saved methods
  - Default payment selection
- **Account Settings**:
  - Email preferences
  - SMS notifications toggle
  - Privacy settings
  - Delete account option

#### **Preferences** Child Page
- **Favorite Products**:
  - Grid of hearted strains and edibles
  - Remove from favorites option
  - Quick add to cart from favorites
- **Strain Preferences**:
  - Preferred THC range slider
  - CBD preference toggle
  - Effects preferences (checkboxes for relaxing, energizing, etc.)
  - Consumption method preferences
- **Shopping Preferences**:
  - Default quantity amounts
  - Auto-reorder settings
  - Preferred delivery times
  - Budget tracking settings
- **Recommendations**:
  - "Based on your purchases" product suggestions
  - New strain recommendations
  - Dosage recommendations based on tolerance

## Mobile Page Variants

Each child page has a corresponding mobile version optimized for touch and smaller screens:

#### **Mobile Flower Page**
- **Vertical Card Layout**: Single column product cards
- **Swipe Navigation**: Horizontal swipe through strain photos
- **Touch-Optimized Filters**: Large tap targets for Indica/Sativa/Hybrid
- **Quick Add**: Swipe-to-add-to-cart gesture
- **Bottom Sheet**: Strain details slide up from bottom

#### **Mobile Edibles Page**
- **Category Tabs**: Horizontal scrolling category pills
- **Product Cards**: Stacked vertically with larger images
- **Dosage Selector**: Large, thumb-friendly dosage buttons
- **Quick View**: Tap and hold for instant preview

#### **Mobile Cart Review Page**
- **Collapsible Items**: Tap to expand item details
- **Swipe Actions**: Swipe left to remove, right to save for later
- **Sticky Total**: Order summary fixed at bottom
- **Thumb Navigation**: Large checkout button

#### **Mobile Cart Checkout Page**
- **Step Progress**: Visual progress indicator at top
- **Auto-fill**: Address autocomplete for mobile keyboards
- **Payment Shortcuts**: Apple Pay/Google Pay prominent
- **One-Thumb Navigation**: All controls in bottom half

#### **Mobile Active Orders Page**
- **Map View**: Full-screen delivery tracking
- **Driver Contact**: Large call/text driver buttons
- **Order Status**: Prominent status cards with icons
- **Pull-to-Refresh**: Update delivery status

#### **Mobile Order History Page**
- **Infinite Scroll**: Load more orders as user scrolls
- **Quick Reorder**: Prominent reorder buttons
- **Order Search**: Sticky search bar at top
- **Swipe Actions**: Swipe to view details or reorder

#### **Mobile Profile Page**
- **Settings Sections**: Collapsible sections for organization
- **Photo Upload**: Camera integration for profile photo
- **Form Optimization**: Mobile-friendly input fields
- **Address Management**: Map integration for delivery addresses

#### **Mobile Preferences Page**
- **Slider Controls**: Touch-friendly THC/CBD range sliders
- **Toggle Switches**: Large toggle switches for preferences
- **Favorite Grid**: Thumbnail grid of favorite products
- **Quick Actions**: One-tap remove from favorites

## Theme & Layout System

### Theme Selection & Usage
The Cannabis Dispensary app uses the **Sage Theme** from the **pre-existing** professional themes collection. 

**⚠️ IMPORTANT**: We are **NOT** creating new themes. We are using existing themes that are already loaded in the template system.

#### **Using Existing Sage Theme Variables**
The Sage theme is already defined in `themes-professional.css.template` and provides these CSS custom properties:

```css
/* Pre-existing Sage Theme Variables - DO NOT MODIFY */
/* These are already available in the template system */
--primary: #10b981;           /* Cannabis green primary */
--accent: #10b981;            /* Cannabis green accent */
--background: #0f172a;        /* Slate dark background */
--surface: #1e293b;           /* Slate surface */
--surface-variant: #334155;   /* Slate surface variant */
--on-surface: #f1f5f9;        /* Slate light text */
--on-surface-variant: #cbd5e1; /* Slate medium text */
--outline: #475569;           /* Slate outline */
```

**How to Use**: 
- Apply theme class: `className="theme-sage"` on root element
- Use Tailwind classes with theme variables: `bg-primary`, `text-primary`, `border-accent`
- Create custom component classes that reference these variables

### Layout Architecture

#### **App Layout Structure**
The app uses the standard AppLayout.tsx template with:
- **Header**: Fixed header with settings and coin balance
- **TabBar**: Bottom navigation with cannabis-specific tabs
- **Main Content**: Scrollable content area between header and footer
- **Background Effects**: Theme-aware visual effects

#### **Tab Configuration**
```jsx
// Cannabis app tabs in TabBar
const cannabisTabs = [
  { id: 'shop', label: 'Shop', icon: '🌿' },
  { id: 'cart', label: 'Cart', icon: '🛒' },
  { id: 'orders', label: 'Orders', icon: '📦' },
  { id: 'account', label: 'Account', icon: '👤' }
];
```

### Page Layout Templates

#### **Desktop Pages (5-Panel ChessboardLayout)**
Each child page uses the ChessboardLayout component:

```jsx
<ChessboardLayout
  topLeft={<div>Actions/Filters</div>}
  top={<div>Search/Navigation</div>}
  topRight={<div>Cart/User Info</div>}
  left={<div>Categories/Filters</div>}
  center={<div>Main Content</div>}
  right={<div>Product Details/Info</div>}
  bottomLeft={<div>Help/Support</div>}
  bottom={<div>Status/Progress</div>}
  bottomRight={<div>Quick Actions</div>}
/>
```

#### **Mobile Pages (3-Panel MobileChessboardLayout)**
Mobile pages use the simplified MobileChessboardLayout:

```jsx
<MobileChessboardLayout
  topPieces={<div>Quick Actions/Status</div>}
  center={<div>Main Content</div>}
  bottomPieces={<div>Navigation/Actions</div>}
/>
```

### Custom Component Classes

**⚠️ IMPORTANT**: After app generation, add these NEW custom classes to the generated `cannabis-app/src/index.css` file:
- **Use ONLY existing theme variables** (--primary, --accent, --surface, etc.) from professional themes
- **Use standard Tailwind classes** that reference theme variables  
- **NO hardcoded colors** - only theme-aware classes
- **Templates are NEVER modified** - only the generated app's CSS

#### **Cannabis-Specific Components**
Add these NEW classes to the generated `cannabis-app/src/index.css`:

```css
/* Cannabis App Component Classes - Use ONLY theme variables */
.cannabis-product-card {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-lg;
  @apply hover:bg-surface-variant/60 hover:border-primary/30 transition-all duration-300;
  @apply group cursor-pointer;
}

/* Strain Type Badges */
.cannabis-strain-indica {
  @apply bg-purple-100 text-purple-800 border border-purple-200;
}

.cannabis-strain-sativa {
  @apply bg-orange-100 text-orange-800 border border-orange-200;
}

.cannabis-strain-hybrid {
  @apply bg-primary/10 text-primary border border-primary/20;
}

/* THC/CBD Indicators */
.cannabis-thc-badge {
  @apply bg-amber-100 text-amber-800 font-bold;
  @apply px-2 py-1 rounded-full text-xs;
}

.cannabis-cbd-badge {
  @apply bg-blue-100 text-blue-800 font-bold;
  @apply px-2 py-1 rounded-full text-xs;
}

/* Action Buttons */
.cannabis-btn-primary {
  @apply bg-primary hover:bg-primary/90 text-primary-foreground;
  @apply transition-colors duration-200 rounded-lg font-medium;
}

.cannabis-btn-add-cart {
  @apply bg-green-600 hover:bg-green-700 text-white;
  @apply rounded-lg px-4 py-2 font-medium transition-colors;
}

/* Age Verification */
.cannabis-age-verify {
  @apply bg-destructive/10 border-destructive/20 text-destructive;
  @apply p-4 rounded-lg border-2;
}
```

### ASCII Page Mockups

#### **Desktop Flower Page Layout**
```
┌─────────────────────────────────────────────────────────┐
│ Cannabis Dispensary App                      ⚙️ 💰 🟢  │ Title Bar
├─────────┬───────────────────────────────┬───────────────┤
│Filter & │      Search & Navigation      │ Cart & User   │ Top Panel
│Sort     │   [🔍 Search] [Filter▼] [⚙️] │ 🛒(3) Profile │ (Page)
├─────────┼───────────────────────────────┼───────────────┤
│Product  │                               │Product Info   │
│Categories│         Product Grid          │& Reviews      │
│         │                               │               │
│• Flower │    ┌───┐ ┌───┐ ┌───┐ ┌───┐    │Selected:      │
│• Edibles│    │🌿 │ │🌿 │ │🌿 │ │🌿 │    │Blue Dream     │ Center
│• Vapes  │    │THC│ │CBD│ │HYB│ │IND│    │THC: 22%       │ Content
│• Carts  │    └───┘ └───┘ └───┘ └───┘    │Effects: ⚡ 💤 │ Area
│         │    ┌───┐ ┌───┐ ┌───┐ ┌───┐    │[Add to Cart]  │
│Age: ✓   │    │🌿 │ │🌿 │ │🌿 │ │🌿 │    │♥ Save         │
│         │    └───┘ └───┘ └───┘ └───┘    │📋 Compare     │
├─────────┼───────────────────────────────┼───────────────┤
│Help &   │     Status & Progress         │Quick Actions  │ Bottom Panel
│Support  │   📦 Delivery: 2-4 hours     │ ♥ Favorites   │ (Page)
│💬 Chat  │   🎯 32 products found       │ 🔄 Refresh    │
└─────────┴───────────────────────────────┴───────────────┘
│ [🌿 Shop] [🛒 Cart] [📦 Orders] [👤 Account]           │ TabBar
└─────────────────────────────────────────────────────────┘
```

#### **Mobile Flower Page Layout**
```
┌─────────────────────────┐
│ [≡] Cannabis App [Cart] │ Header
├─────────────────────────┤
│ [🔍] [Filter] [Sort]   │ Top Pieces
├─────────────────────────┤
│                         │
│    ┌─────────────────┐  │
│    │ 🌿 Blue Dream   │  │
│    │ THC: 22% | Hybrid│  │
│    │ $45/eighth      │  │
│    │ [Add to Cart]   │  │
│    └─────────────────┘  │
│                         │
│    ┌─────────────────┐  │ Main Content
│    │ 🌿 Girl Scout   │  │ (Scrollable)
│    │ THC: 25% | Hybrid│  │
│    │ $50/eighth      │  │
│    │ [Add to Cart]   │  │
│    └─────────────────┘  │
│                         │
│    [Load More...]       │
├─────────────────────────┤
│ ♥ Favorites | 🔍 Search │ Bottom Pieces
├─────────────────────────┤
│[🌿][🛒][📦][👤]         │ TabBar
└─────────────────────────┘
```

### Component Integration Guidelines
- **Theme Variables**: Use CSS custom properties exclusively (no hardcoded colors)
- **Layout Components**: Leverage ChessboardLayout and MobileChessboardLayout
- **Glass Effects**: Apply `.card-gaming` for content cards, `.glass-layout` for navigation
- **Responsive Design**: Automatic switching between desktop and mobile layouts
- **Cannabis Branding**: Maintain green theme with appropriate cannabis iconography

## Implementation Commands

### Phase 1: Create Base Application

```bash
# Navigate to the template-tests-v2 directory
cd /mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2

# Create base application with Vite + React + Tailwind + HeadlessUI + Icons
npm create vite@latest base-app -- --template react-ts
cd base-app

# Install base dependencies
npm install

# Install Tailwind CSS and related packages
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install HeadlessUI components
npm install @headlessui/react

# Install icon libraries
npm install lucide-react react-icons

# Test base app builds successfully
npm run build

# Return to parent directory
cd ..
```

### Phase 2: Setup Cannabis App Directory

```bash
# Copy base app structure (excluding src folder) to cannabis-app
mkdir -p cannabis-app
cp -r base-app/{package.json,package-lock.json,vite.config.ts,tsconfig.json,tsconfig.node.json,tailwind.config.js,postcss.config.js,index.html,public} cannabis-app/

# Navigate to cannabis app directory
cd cannabis-app

# Install dependencies in cannabis app
npm install
```

### Phase 3: Generate Cannabis App Pages

```bash
# Navigate back to generator directory
cd cannabis-app

# Create parent pages
npm run mobile -- parent Shop
npm run mobile -- parent Cart  
npm run mobile -- parent Orders
npm run mobile -- parent Account

# Create child pages with mobile variants under Shop parent
npm run mobile -- child Flower --parent shop npm run mobile -- child Edibles --parent shop 
# Create child pages with mobile variants under Cart parent
npm run mobile -- child Review --parent cart npm run mobile -- child Checkout --parent cart 
# Create child pages with mobile variants under Orders parent
npm run mobile -- child Active --parent orders npm run mobile -- child History --parent orders 
# Create child pages with mobile variants under Account parent
npm run mobile -- child Profile --parent account npm run mobile -- child Preferences --parent account ```

## File Structure Tree

```
cannabis-app/
├── src/
│   ├── components/
│   │   ├── shop/
│   │   │   ├── FlowerPageWrapper.tsx
│   │   │   ├── EdiblesPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── cart/
│   │   │   ├── ReviewPageWrapper.tsx
│   │   │   ├── CheckoutPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── orders/
│   │   │   ├── ActivePageWrapper.tsx
│   │   │   ├── HistoryPageWrapper.tsx
│   │   │   └── index.ts
│   │   └── account/
│   │       ├── ProfilePageWrapper.tsx
│   │       ├── PreferencesPageWrapper.tsx
│   │       └── index.ts
│   ├── pages/
│   │   ├── shop/
│   │   │   ├── ShopPage.tsx
│   │   │   ├── ShopMainPage.tsx
│   │   │   ├── FlowerPage.tsx
│   │   │   ├── MobileFlowerPage.tsx
│   │   │   ├── EdiblesPage.tsx
│   │   │   └── MobileEdiblesPage.tsx
│   │   ├── cart/
│   │   │   ├── CartPage.tsx
│   │   │   ├── CartMainPage.tsx
│   │   │   ├── ReviewPage.tsx
│   │   │   ├── MobileReviewPage.tsx
│   │   │   ├── CheckoutPage.tsx
│   │   │   └── MobileCheckoutPage.tsx
│   │   ├── orders/
│   │   │   ├── OrdersPage.tsx
│   │   │   ├── OrdersMainPage.tsx
│   │   │   ├── ActivePage.tsx
│   │   │   ├── MobileActivePage.tsx
│   │   │   ├── HistoryPage.tsx
│   │   │   └── MobileHistoryPage.tsx
│   │   └── account/
│   │       ├── AccountPage.tsx
│   │       ├── AccountMainPage.tsx
│   │       ├── ProfilePage.tsx
│   │       ├── MobileProfilePage.tsx
│   │       ├── PreferencesPage.tsx
│   │       └── MobilePreferencesPage.tsx
│   ├── hooks/
│   │   ├── shop/
│   │   │   └── useShopActions.ts
│   │   ├── cart/
│   │   │   └── useCartActions.ts
│   │   ├── orders/
│   │   │   └── useOrdersActions.ts
│   │   └── account/
│   │       └── useAccountActions.ts
│   ├── services/
│   │   ├── api/
│   │   │   ├── productsApi.ts
│   │   │   ├── cartApi.ts
│   │   │   ├── ordersApi.ts
│   │   │   └── userApi.ts
│   │   └── instructions/
│   │       └── pages/
│   │           ├── shop.ts
│   │           ├── cart.ts
│   │           ├── orders.ts
│   │           └── account.ts
│   ├── constants/
│   │   └── actions/
│   │       └── pages/
│   │           ├── shop.ts
│   │           ├── cart.ts
│   │           ├── orders.ts
│   │           └── account.ts
│   └── types/
│       ├── products.ts
│       ├── cart.ts
│       ├── orders.ts
│       └── user.ts
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
    date_of_birth DATE,
    verified_age BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Addresses table
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    type VARCHAR(20) DEFAULT 'delivery', -- delivery, billing
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    instructions TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Product categories
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL, -- flower, edibles, concentrates
    description TEXT,
    active BOOLEAN DEFAULT TRUE
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    strain_type VARCHAR(20), -- indica, sativa, hybrid
    thc_percentage DECIMAL(5,2),
    cbd_percentage DECIMAL(5,2),
    effects TEXT[], -- array of effects
    price_per_gram DECIMAL(10,2),
    price_per_eighth DECIMAL(10,2),
    in_stock BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Cart table
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_type VARCHAR(20) DEFAULT 'gram', -- gram, eighth, quarter
    added_at TIMESTAMP DEFAULT NOW()
);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    address_id INTEGER REFERENCES addresses(id),
    status VARCHAR(50) DEFAULT 'pending', -- pending, confirmed, preparing, out_for_delivery, delivered, cancelled
    subtotal DECIMAL(10,2) NOT NULL,
    delivery_fee DECIMAL(10,2) DEFAULT 0,
    tax DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    estimated_delivery TIMESTAMP,
    delivered_at TIMESTAMP,
    driver_id INTEGER,
    tracking_data JSONB, -- GPS coordinates, status updates
    created_at TIMESTAMP DEFAULT NOW()
);

-- Order items table
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_type VARCHAR(20),
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL
);

-- User preferences
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) UNIQUE,
    preferred_thc_min DECIMAL(5,2),
    preferred_thc_max DECIMAL(5,2),
    preferred_cbd BOOLEAN DEFAULT FALSE,
    favorite_effects TEXT[],
    preferred_delivery_time VARCHAR(50),
    auto_reorder BOOLEAN DEFAULT FALSE,
    notifications_enabled BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Favorites table
CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, product_id)
);
```

## API Routes

### Authentication Routes
```
POST   /api/auth/register        # User registration with age verification
POST   /api/auth/login           # User login
POST   /api/auth/logout          # User logout
POST   /api/auth/verify-age      # Age verification process
```

### Product Routes (Shop Pages)
```
GET    /api/products             # Get all products with filters
GET    /api/products/flower      # Get flower products only
GET    /api/products/edibles     # Get edibles products only
GET    /api/products/:id         # Get single product details
GET    /api/categories           # Get product categories
GET    /api/products/search      # Search products by name/effects
```

### Cart Routes (Cart Pages)
```
GET    /api/cart                 # Get user's cart items
POST   /api/cart/add             # Add item to cart
PUT    /api/cart/update/:id      # Update cart item quantity
DELETE /api/cart/remove/:id      # Remove item from cart
DELETE /api/cart/clear           # Clear entire cart
POST   /api/cart/checkout        # Process checkout
```

### Order Routes (Orders Pages)
```
GET    /api/orders               # Get user's order history
GET    /api/orders/active        # Get active orders
GET    /api/orders/:id           # Get specific order details
GET    /api/orders/:id/tracking  # Get delivery tracking info
POST   /api/orders/:id/reorder   # Reorder previous order
```

### User Routes (Account Pages)
```
GET    /api/user/profile         # Get user profile
PUT    /api/user/profile         # Update user profile
GET    /api/user/addresses       # Get user addresses
POST   /api/user/addresses       # Add new address
PUT    /api/user/addresses/:id   # Update address
DELETE /api/user/addresses/:id   # Delete address
GET    /api/user/preferences     # Get user preferences
PUT    /api/user/preferences     # Update preferences
GET    /api/user/favorites       # Get favorite products
POST   /api/user/favorites       # Add product to favorites
DELETE /api/user/favorites/:id   # Remove from favorites
```

### Delivery Routes
```
GET    /api/delivery/estimate    # Get delivery time estimate
GET    /api/delivery/areas       # Get serviceable areas
POST   /api/delivery/schedule    # Schedule delivery time
```

## Key Features
- Clean product cards with strain photos
- Simple quantity selectors
- Delivery ETA calculator
- Age verification modal on first visit
- Favorite products heart icon
- Reorder from history functionality

## Technical Implementation
- Product data stored in simple JSON
- Mock delivery tracking with fake GPS coordinates
- Local storage for cart and favorites
- No real payment processing (demo only)
- Responsive design for mobile-first experience

## Demo Highlights
- Browse flower strains with beautiful product photos
- Add items to cart with quantity controls
- Mock checkout flow with address entry
- Live delivery tracking simulation
- Professional, legitimate feeling design