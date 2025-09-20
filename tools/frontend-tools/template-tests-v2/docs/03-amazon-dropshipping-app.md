# 03 - Amazon-Style Dropshipping App MVP

## Implementation Plan

### Phase 1: Base Application Setup
This app uses the shared base React Vite application with all required dependencies:

1. **Base App Foundation** from `/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/base-app`
   - Vanilla React + Vite + TypeScript
   - Tailwind CSS 3.x
   - HeadlessUI components
   - Lucide React icons
   - React Icons library

2. **Marketplace App Setup** - Copy base app structure (excluding src) to create marketplace-app directory

3. **Page Generation** - Use template-based generator to create complete marketplace structure

### Phase 2: Marketplace App Generation
Use the template-based generator to create the complete marketplace app structure on top of the base app foundation.

## App Vision
A comprehensive marketplace app for buying everything from electronics to home goods. Think "Amazon simplified" with product reviews, recommendations, multiple sellers, and fast checkout experience.

## What Makes This Special
- **Multi-seller marketplace** - Different vendors for same products
- **Smart recommendations** - "People who bought this also bought"
- **Review system** - Star ratings, photos, verified purchases
- **Deal hunting** - Daily deals, lightning sales, price drops

## Parent Pages & Children

### 1. **Browse** Parent
**Purpose**: Discover and search products across categories

#### **Categories** Child Page
- **Main Category Grid**: Large visual tiles for major categories
  - Electronics, Home & Garden, Fashion, Books, Sports, Beauty, Toys
  - Category images with item count badges
  - Trending indicators for hot categories
- **Featured Products Carousel**: 
  - Rotating showcase of featured items from each category
  - Product images, prices, ratings
  - Quick view and add to cart options
- **Category Detail View**: When category selected
  - Subcategory navigation (Electronics → Phones, Laptops, Audio)
  - Filter sidebar (brand, price range, ratings, shipping)
  - Product grid with infinite scroll
  - Sort options (relevance, price, ratings, newest)
- **Product Cards Include**:
  - High-quality product images
  - Product title and brand
  - Star rating (out of 5) with review count
  - Price with discount indicators
  - Prime/fast shipping badges
  - Multiple seller indicators
  - Add to cart and wishlist buttons
- **Category-Specific Features**:
  - Size charts for fashion
  - Compatibility filters for electronics
  - Age ranges for toys
  - Ingredient lists for beauty/health

#### **Deals** Child Page
- **Deal of the Day Banner**: 
  - Countdown timer for daily featured deal
  - Large product image and discount percentage
  - Limited quantity indicator
- **Lightning Deals Section**:
  - Grid of time-sensitive offers
  - Progress bars showing claim percentage
  - Countdown timers for each deal
  - "Claim" buttons with instant add to cart
- **Clearance Section**:
  - Heavily discounted items
  - Final sale indicators
  - Limited stock warnings
  - Category-based clearance browsing
- **Price Drop Alerts**:
  - Recently reduced items
  - Previous price vs. current price
  - Percentage saved indicators
- **Coupon Center**:
  - Available discount coupons
  - Clip to activate functionality
  - Category-specific coupons
  - Expiration date tracking
- **Bundle Deals**:
  - Buy 2 get 1 free offers
  - Complementary product bundles
  - Total savings calculations

### 2. **Search** Parent
**Purpose**: Find specific products with filters

#### **Results** Child Page
- **Search Bar**: 
  - Auto-complete suggestions
  - Voice search capability
  - Recent searches dropdown
  - Search within results option
- **Filter Sidebar**:
  - Price range slider
  - Brand checkboxes with item counts
  - Customer rating filters (4+ stars, 3+ stars)
  - Shipping options (Prime, Free shipping)
  - Availability (In stock, Used, New)
  - Color/size options for applicable products
- **Sort Controls**:
  - Relevance, price low to high, price high to low
  - Customer reviews, newest arrivals
  - Best sellers, deals and promotions
- **Search Results Grid**:
  - Product cards with enhanced info
  - Sponsored product indicators
  - Multiple seller comparison
  - Quick comparison checkboxes
- **Product Comparison**:
  - Side-by-side comparison table
  - Feature comparison matrix
  - Price and seller comparison
- **Search Refinement**:
  - "Did you mean?" suggestions
  - Related search terms
  - Category suggestions
  - Search result count indicators

#### **Suggestions** Child Page
- **Related Searches**:
  - Popular related search terms
  - Trending searches in category
  - Recently searched by others
- **Recommended Products**:
  - "Customers who searched for X also bought"
  - AI-powered product suggestions
  - Similar items with better ratings
  - Alternative brands/options
- **Browse History**:
  - Recently viewed products
  - Continue shopping from where left off
  - Clear history option
- **Popular in Your Area**:
  - Locally trending products
  - Fast delivery options
  - Regional preferences
- **Seasonal Suggestions**:
  - Holiday-related products
  - Weather-appropriate items
  - Trending seasonal categories
- **Brand Discovery**:
  - Featured brand spotlights
  - New brand introductions
  - Brand comparison tools

### 3. **Cart** Parent
**Purpose**: Shopping cart and checkout process

#### **Review** Child Page
- **Cart Items List**: Each item shows:
  - Product image and title
  - Selected options (size, color, variant)
  - Seller information and ratings
  - Individual item price
  - Quantity selector with availability check
  - Remove and save for later options
  - Estimated delivery date
- **Multi-Seller Organization**:
  - Items grouped by seller
  - Individual shipping costs per seller
  - Combined shipping opportunities
  - Seller rating and fulfillment info
- **Order Summary Panel**:
  - Items subtotal
  - Shipping costs breakdown
  - Tax calculations
  - Discount/coupon applications
  - Final total with prominent display
- **Shipping Estimates**:
  - Delivery date calculator
  - Address-based shipping options
  - Express shipping upgrades
- **Recommendations**:
  - "Frequently bought together"
  - Complementary product suggestions
  - Accessories for cart items
- **Save for Later**:
  - Move items to wishlist
  - Price tracking for saved items
  - Stock notifications

#### **Checkout** Child Page
- **Shipping Address**:
  - Address book with saved addresses
  - New address form with validation
  - Address suggestions and autocomplete
  - Delivery instructions field
- **Delivery Options**:
  - Standard delivery with dates
  - Express/next-day options
  - Pickup point selections
  - Delivery time slot booking
- **Payment Methods**:
  - Saved payment cards
  - New card entry with security
  - Digital wallet options (PayPal, Apple Pay)
  - Buy now, pay later options
- **Order Review**:
  - Final item verification
  - Shipping address confirmation
  - Payment method verification
  - Total cost breakdown
- **Promotional Codes**:
  - Coupon code entry
  - Available discount application
  - Gift card balance usage
- **Place Order**:
  - Order confirmation
  - Estimated delivery summary
  - Order tracking setup

### 4. **Account** Parent
**Purpose**: User profile and order management

#### **Orders** Child Page
- **Order History**: Each order displays:
  - Order number and placement date
  - Order status with progress tracking
  - Total amount and item count
  - Product thumbnails
  - Delivery status and tracking
  - Invoice/receipt download
  - Reorder and review options
- **Active Orders Section**:
  - Currently processing orders
  - Shipping updates and tracking
  - Delivery progress with maps
  - Modify/cancel options (if applicable)
- **Order Tracking**:
  - Real-time package tracking
  - Delivery route visualization
  - Photo proof of delivery
  - Delivery feedback options
- **Returns & Exchanges**:
  - Return request initiation
  - Return policy information
  - Prepaid return labels
  - Exchange options and process
  - Refund status tracking
- **Order Issues**:
  - Report problems with orders
  - Missing items claims
  - Damaged product reports
  - Customer service chat integration
- **Digital Orders**:
  - E-book and digital downloads
  - Software license management
  - Subscription service access

#### **Lists** Child Page
- **Wishlists Management**:
  - Multiple wishlist creation
  - Public/private list settings
  - Share wishlist functionality
  - Move between lists
- **Saved for Later**:
  - Items moved from cart
  - Price tracking and alerts
  - Stock availability notifications
  - Quick move to cart
- **Recently Viewed**:
  - Browsing history with timestamps
  - Continue shopping suggestions
  - Clear history options
  - Product comparison from history
- **Gift Lists**:
  - Registry creation for events
  - Gift idea suggestions
  - Contributor tracking
  - Thank you note management
- **List Organization**:
  - Category-based list sorting
  - Priority levels for items
  - Notes and comments on products
  - Due date reminders for gifts
- **Price Alerts**:
  - Set price drop notifications
  - Deal alerts for list items
  - Stock availability alerts
  - Sale event notifications

## Theme & Layout System

### Gold Theme
This app uses the **Gold** theme from the professional themes collection, providing a premium, luxury marketplace aesthetic that conveys trust and quality.

**Theme Variables (Gold):**
```css
/* Gold Theme Variables */
--primary: #eab308;           /* Gold yellow primary */
--accent: #eab308;            /* Gold yellow accent */
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
- **Browse** - Grid icon (Categories, Deals)
- **Search** - Search icon (Results, Suggestions)
- **Cart** - Shopping cart icon (Review, Checkout)
- **Account** - User icon (Orders, Lists)

### Layout Templates

#### Desktop Pages (ChessboardLayout)
5-panel design for comprehensive marketplace browsing:
```jsx
<ChessboardLayout
  topLeft={<div className="marketplace-filters">Filters/Categories</div>}
  top={<div className="marketplace-search">Search/Navigation</div>}
  topRight={<div className="marketplace-account">Account/Cart Info</div>}
  left={<div className="marketplace-sidebar">Deals/Recommendations</div>}
  center={<div className="marketplace-products">Product Grid/Details</div>}
  right={<div className="marketplace-details">Product/Seller Info</div>}
  bottomLeft={<div className="marketplace-tools">Comparison Tools</div>}
  bottom={<div className="marketplace-status">Order/Shipping Status</div>}
  bottomRight={<div className="marketplace-actions">Quick Actions</div>}
/>
```

#### Mobile Pages (MobileChessboardLayout)
3-panel design optimized for mobile shopping:
```jsx
<MobileChessboardLayout
  topPieces={<div className="marketplace-mobile-header">Search/Account</div>}
  center={<div className="marketplace-mobile-content">Product Grid/Details</div>}
  bottomPieces={<div className="marketplace-mobile-actions">Cart/Actions</div>}
/>
```

### Custom Component Classes

**⚠️ IMPORTANT**: After app generation, add these NEW custom classes to the generated `marketplace-app/src/index.css` file:
- **Use ONLY existing theme variables** (--primary, --accent, --surface, etc.) from professional themes
- **Use standard Tailwind classes** that reference theme variables
- **NO hardcoded colors** - only theme-aware classes
- **Templates are NEVER modified** - only the generated app's CSS

Add these NEW classes to the generated `marketplace-app/src/index.css`:

```css
/* Marketplace App Component Classes */
.marketplace-product-card {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-lg overflow-hidden;
  @apply hover:bg-surface-variant/60 hover:border-primary/30 hover:shadow-lg transition-all duration-300;
  @apply group cursor-pointer;
}

.marketplace-product-image {
  @apply aspect-square w-full object-cover;
  @apply group-hover:scale-105 transition-transform duration-300;
}

.marketplace-star-rating {
  @apply flex items-center gap-1 text-primary;
}

.marketplace-price-display {
  @apply text-primary font-bold text-lg;
}

.marketplace-deal-badge {
  @apply bg-primary/20 text-primary px-2 py-1 rounded-full text-xs font-semibold;
  @apply border border-primary/30;
}

.marketplace-seller-card {
  @apply bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply hover:bg-surface-variant/40 transition-colors;
}

.marketplace-filter-panel {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply space-y-4;
}

.marketplace-cart-item {
  @apply flex gap-4 p-4 bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-lg;
  @apply hover:bg-surface-variant/40 transition-colors;
}

.marketplace-category-tile {
  @apply bg-gradient-to-br from-primary/20 to-accent/10;
  @apply border border-primary/30 rounded-xl p-6 text-center;
  @apply hover:from-primary/30 hover:to-accent/20 transition-all duration-300;
  @apply cursor-pointer group;
}

.marketplace-deal-countdown {
  @apply bg-primary/20 text-primary px-3 py-2 rounded-lg font-mono text-sm;
  @apply border border-primary/30;
}

.marketplace-wishlist-button {
  @apply p-2 rounded-full bg-surface/80 backdrop-blur-sm;
  @apply hover:bg-primary/20 hover:text-primary transition-all;
  @apply data-[wishlisted=true]:bg-primary/20 data-[wishlisted=true]:text-primary;
}

.marketplace-review-card {
  @apply bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply space-y-3;
}
```

### ASCII Mockups

#### Desktop Layout (ChessboardLayout)
```
┌─────────────────────────────────────────────────────────────────┐
│                   Amazon-Style Marketplace App                 │
├─────────┬─────────────────────────┬─────────────────────────────┤
│Filters/ │    Search/Navigation    │    Account/Cart Info        │
│Category │                         │                             │
├─────────┼─────────────────────────┼─────────────────────────────┤
│         │                         │                             │
│ Deals/  │                         │   Product/Seller Info       │
│Recommend│    Product Grid/Details │                             │
│ations   │                         │                             │
│         │                         │                             │
├─────────┼─────────────────────────┼─────────────────────────────┤
│Compare  │  Order/Shipping Status  │    Quick Actions            │
│ Tools   │                         │                             │
├─────────┴─────────────────────────┴─────────────────────────────┤
│                          TabBar                                 │
│     Browse    Search     Cart     Account                       │
└─────────────────────────────────────────────────────────────────┘
```

#### Mobile Layout (MobileChessboardLayout)
```
┌─────────────────────────────────┐
│     Amazon-Style Marketplace   │
├─────────────────────────────────┤
│       Search/Account            │
│                                 │
├─────────────────────────────────┤
│                                 │
│                                 │
│    Product Grid/Details         │
│                                 │
│                                 │
├─────────────────────────────────┤
│       Cart/Actions              │
│                                 │
├─────────────────────────────────┤
│             TabBar              │
│  Browse  Search  Cart  Account  │
└─────────────────────────────────┘
```

## Key Features
- Product cards with star ratings and reviews
- Multi-seller comparison for same products
- Advanced filtering (price, brand, rating, shipping)
- One-click add to cart functionality
- Wishlist and save for later
- Order tracking with delivery updates
- Product recommendation engine
- Review photos and Q&A sections

## Technical Implementation
- Complex product data with multiple sellers
- Star rating components and review displays
- Shopping cart with multi-seller handling
- Advanced search with filter combinations
- Mock payment and shipping calculations
- Order status simulation with tracking
- Recommendation algorithm simulation

## Demo Highlights
- Browse thousands of products across categories
- Compare prices from different sellers
- Advanced search with multiple filters
- Smart product recommendations
- Multi-seller cart with shipping calculations
- Order tracking with delivery simulation

## Mobile Page Variants

Each child page has a corresponding mobile version optimized for touch and smaller screens:

#### **Mobile Categories Page**
- **Vertical Category List**: Single column layout for easy browsing
- **Touch Navigation**: Large tap targets for category selection
- **Swipe Filters**: Horizontal swipe through filter options
- **Quick Search**: Prominent search bar at top
- **Touch Product Cards**: Mobile-optimized product cards with large images

#### **Mobile Deals Page**
- **Deal Stack**: Vertical stack of deal cards for mobile
- **Countdown Timers**: Prominent timers for time-sensitive deals
- **Swipe Actions**: Swipe to claim deals or add to cart
- **Touch Coupons**: One-tap coupon claiming
- **Mobile Notifications**: Push notification setup for deal alerts

#### **Mobile Search Results Page**
- **Vertical Results**: Single column search results
- **Filter Drawer**: Slide-out filter panel from bottom
- **Touch Sort**: Easy sort options with large buttons
- **Quick View**: Tap and hold for product quick view
- **Voice Search**: Mobile voice search integration

#### **Mobile Search Suggestions Page**
- **Touch History**: Large touch targets for search history
- **Swipe Suggestions**: Horizontal swipe through suggestions
- **Quick Actions**: One-tap search execution
- **Mobile Recommendations**: Touch-friendly recommendation cards

#### **Mobile Cart Review Page**
- **Vertical Cart Items**: Single column cart layout
- **Swipe Management**: Swipe to remove or save for later
- **Seller Grouping**: Collapsible seller sections
- **Touch Quantity**: Large +/- buttons for quantity
- **Sticky Checkout**: Fixed checkout button at bottom

#### **Mobile Cart Checkout Page**
- **Step Progress**: Mobile checkout progress indicator
- **Form Optimization**: Mobile-friendly form fields
- **Address Auto**: GPS and autocomplete integration
- **Payment Quick**: Apple Pay/Google Pay prominent placement
- **Touch Review**: Easy order review with tap to edit

#### **Mobile Orders Page**
- **Order Cards**: Mobile-optimized order cards
- **Touch Tracking**: Tap to expand tracking details
- **Swipe Actions**: Swipe to reorder or view details
- **Mobile Timeline**: Touch-friendly order status updates
- **Quick Contact**: One-tap seller contact

#### **Mobile Lists Page**
- **Grid Wishlist**: Mobile-optimized wishlist grid
- **Quick Actions**: One-tap move to cart or remove
- **List Management**: Touch-friendly list organization
- **Share Options**: Mobile sharing for lists
- **Touch Reorder**: Easy reordering with drag and drop

## Implementation Commands

### Phase 1: Setup Marketplace App Directory

```bash
# Copy base app structure (excluding src folder) to marketplace-app
cd /mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2
mkdir -p marketplace-app
cp -r base-app/{package.json,package-lock.json,vite.config.ts,tsconfig.json,tsconfig.node.json,tailwind.config.js,postcss.config.js,index.html,public} marketplace-app/

# Navigate to marketplace app directory and install dependencies
cd marketplace-app
npm install
cd ..
```

### Phase 2: Generate Marketplace App Pages

```bash
# Navigate to generator directory
cd marketplace-app

# Create parent pages
npm run mobile -- parent Browse
npm run mobile -- parent Search
npm run mobile -- parent Cart
npm run mobile -- parent Account

# Create child pages with mobile variants under Browse parent
npm run mobile -- child Categories --parent browse npm run mobile -- child Deals --parent browse 
# Create child pages with mobile variants under Search parent
npm run mobile -- child Results --parent search npm run mobile -- child Suggestions --parent search 
# Create child pages with mobile variants under Cart parent
npm run mobile -- child Review --parent cart npm run mobile -- child Checkout --parent cart 
# Create child pages with mobile variants under Account parent
npm run mobile -- child Orders --parent account npm run mobile -- child Lists --parent account ```

## File Structure Tree

```
marketplace-app/
├── src/
│   ├── components/
│   │   ├── browse/
│   │   │   ├── CategoriesPageWrapper.tsx
│   │   │   ├── DealsPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── search/
│   │   │   ├── ResultsPageWrapper.tsx
│   │   │   ├── SuggestionsPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── cart/
│   │   │   ├── ReviewPageWrapper.tsx
│   │   │   ├── CheckoutPageWrapper.tsx
│   │   │   └── index.ts
│   │   └── account/
│   │       ├── OrdersPageWrapper.tsx
│   │       ├── ListsPageWrapper.tsx
│   │       └── index.ts
│   ├── pages/
│   │   ├── browse/
│   │   │   ├── BrowsePage.tsx
│   │   │   ├── BrowseMainPage.tsx
│   │   │   ├── CategoriesPage.tsx
│   │   │   ├── MobileCategoriesPage.tsx
│   │   │   ├── DealsPage.tsx
│   │   │   └── MobileDealsPage.tsx
│   │   ├── search/
│   │   │   ├── SearchPage.tsx
│   │   │   ├── SearchMainPage.tsx
│   │   │   ├── ResultsPage.tsx
│   │   │   ├── MobileResultsPage.tsx
│   │   │   ├── SuggestionsPage.tsx
│   │   │   └── MobileSuggestionsPage.tsx
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
│   │       ├── ListsPage.tsx
│   │       └── MobileListsPage.tsx
│   ├── hooks/
│   │   ├── browse/
│   │   │   └── useBrowseActions.ts
│   │   ├── search/
│   │   │   └── useSearchActions.ts
│   │   ├── cart/
│   │   │   └── useCartActions.ts
│   │   └── account/
│   │       └── useAccountActions.ts
│   ├── services/
│   │   ├── api/
│   │   │   ├── productsApi.ts
│   │   │   ├── searchApi.ts
│   │   │   ├── cartApi.ts
│   │   │   ├── ordersApi.ts
│   │   │   └── sellersApi.ts
│   │   └── instructions/
│   │       └── pages/
│   │           ├── browse.ts
│   │           ├── search.ts
│   │           ├── cart.ts
│   │           └── account.ts
│   ├── constants/
│   │   └── actions/
│   │       └── pages/
│   │           ├── browse.ts
│   │           ├── search.ts
│   │           ├── cart.ts
│   │           └── account.ts
│   └── types/
│       ├── products.ts
│       ├── sellers.ts
│       ├── cart.ts
│       ├── orders.ts
│       └── deals.ts
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
    address JSONB, -- default shipping address
    prime_member BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Sellers table
CREATE TABLE sellers (
    id SERIAL PRIMARY KEY,
    business_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    logo_url VARCHAR(500),
    rating DECIMAL(3,2) DEFAULT 0.00, -- average rating
    total_reviews INTEGER DEFAULT 0,
    fulfillment_method VARCHAR(50) DEFAULT 'merchant', -- merchant, amazon, dropship
    shipping_regions TEXT[], -- regions they ship to
    return_policy TEXT,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL, -- Electronics, Home, Fashion, etc.
    description TEXT,
    image_url VARCHAR(500),
    parent_category_id INTEGER REFERENCES categories(id),
    level INTEGER DEFAULT 1, -- 1=main, 2=sub, 3=sub-sub
    sort_order INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT TRUE
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    brand VARCHAR(100),
    model VARCHAR(100),
    main_image_url VARCHAR(500),
    image_urls TEXT[], -- additional product images
    specifications JSONB, -- technical specs
    features TEXT[], -- key features
    dimensions JSONB, -- size, weight, etc.
    base_price DECIMAL(10,2) NOT NULL, -- MSRP or base price
    avg_rating DECIMAL(3,2) DEFAULT 0.00,
    total_reviews INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Product listings (seller-specific pricing and availability)
CREATE TABLE product_listings (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    seller_id INTEGER REFERENCES sellers(id),
    condition VARCHAR(50) DEFAULT 'new', -- new, used, refurbished
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    shipping_cost DECIMAL(8,2) DEFAULT 0.00,
    prime_eligible BOOLEAN DEFAULT FALSE,
    estimated_delivery_days INTEGER DEFAULT 7,
    warranty_info TEXT,
    return_window INTEGER DEFAULT 30, -- days
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(product_id, seller_id, condition)
);

-- Shopping cart
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    listing_id INTEGER REFERENCES product_listings(id),
    quantity INTEGER DEFAULT 1,
    added_at TIMESTAMP DEFAULT NOW()
);

-- Orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, confirmed, shipped, delivered, cancelled
    subtotal DECIMAL(10,2) NOT NULL,
    shipping_cost DECIMAL(10,2) DEFAULT 0.00,
    tax DECIMAL(10,2) DEFAULT 0.00,
    total DECIMAL(10,2) NOT NULL,
    shipping_address JSONB NOT NULL,
    payment_method JSONB NOT NULL,
    estimated_delivery DATE,
    tracking_numbers JSONB, -- can have multiple packages
    created_at TIMESTAMP DEFAULT NOW(),
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP
);

-- Order items (can be from multiple sellers)
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    listing_id INTEGER REFERENCES product_listings(id),
    seller_id INTEGER REFERENCES sellers(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    fulfillment_status VARCHAR(50) DEFAULT 'pending', -- pending, shipped, delivered
    tracking_number VARCHAR(100)
);

-- Product reviews
CREATE TABLE product_reviews (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    user_id INTEGER REFERENCES users(id),
    order_item_id INTEGER REFERENCES order_items(id), -- for verified purchases
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(200),
    review_text TEXT,
    review_images TEXT[], -- photo reviews
    verified_purchase BOOLEAN DEFAULT FALSE,
    helpful_votes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Seller reviews
CREATE TABLE seller_reviews (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER REFERENCES sellers(id),
    user_id INTEGER REFERENCES users(id),
    order_id INTEGER REFERENCES orders(id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Wishlists and saved items
CREATE TABLE wishlists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) DEFAULT 'My Wishlist',
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE wishlist_items (
    id SERIAL PRIMARY KEY,
    wishlist_id INTEGER REFERENCES wishlists(id),
    product_id INTEGER REFERENCES products(id),
    preferred_listing_id INTEGER REFERENCES product_listings(id), -- preferred seller
    added_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(wishlist_id, product_id)
);

-- Deals and promotions
CREATE TABLE deals (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    deal_type VARCHAR(50) NOT NULL, -- lightning, daily, clearance, coupon
    listing_id INTEGER REFERENCES product_listings(id),
    original_price DECIMAL(10,2) NOT NULL,
    deal_price DECIMAL(10,2) NOT NULL,
    discount_percentage DECIMAL(5,2),
    quantity_available INTEGER,
    quantity_claimed INTEGER DEFAULT 0,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- User browsing history
CREATE TABLE browsing_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    viewed_at TIMESTAMP DEFAULT NOW()
);

-- Search history
CREATE TABLE search_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    search_query VARCHAR(500),
    results_count INTEGER,
    searched_at TIMESTAMP DEFAULT NOW()
);
```

## API Routes

### Authentication Routes
```
POST   /api/auth/register        # User registration
POST   /api/auth/login           # User login
POST   /api/auth/logout          # User logout
```

### Browse Routes (Browse Pages)
```
GET    /api/browse/categories    # Get all categories with hierarchy
GET    /api/browse/category/:id  # Get products in category
GET    /api/browse/deals         # Get current deals and promotions
GET    /api/browse/deals/lightning # Get lightning deals
GET    /api/browse/deals/daily   # Get daily deals
GET    /api/browse/featured      # Get featured products
GET    /api/browse/bestsellers   # Get bestselling products
```

### Search Routes (Search Pages)
```
GET    /api/search               # Search products with filters
GET    /api/search/suggestions   # Get search suggestions
GET    /api/search/autocomplete  # Get autocomplete results
GET    /api/search/history       # Get user's search history
DELETE /api/search/history       # Clear search history
GET    /api/search/filters       # Get available filters for search
```

### Product Routes
```
GET    /api/products/:id         # Get product details
GET    /api/products/:id/listings # Get all seller listings for product
GET    /api/products/:id/reviews # Get product reviews
GET    /api/products/:id/questions # Get product Q&A
GET    /api/products/:id/recommendations # Get recommended products
GET    /api/products/compare     # Compare multiple products
```

### Cart Routes (Cart Pages)
```
GET    /api/cart                 # Get user's cart items
POST   /api/cart/add             # Add item to cart
PUT    /api/cart/update/:id      # Update cart item quantity
DELETE /api/cart/remove/:id      # Remove item from cart
DELETE /api/cart/clear           # Clear entire cart
POST   /api/cart/save-later/:id  # Save item for later
GET    /api/cart/saved           # Get saved for later items
POST   /api/cart/checkout        # Process checkout
```

### Order Routes (Account Pages)
```
GET    /api/orders               # Get user's order history
GET    /api/orders/:id           # Get specific order details
GET    /api/orders/:id/tracking  # Get order tracking information
POST   /api/orders/:id/cancel    # Cancel order (if possible)
POST   /api/orders/:id/return    # Initiate return
GET    /api/orders/active        # Get active/current orders
```

### Wishlist Routes (Account Pages)
```
GET    /api/wishlists            # Get user's wishlists
POST   /api/wishlists            # Create new wishlist
PUT    /api/wishlists/:id        # Update wishlist
DELETE /api/wishlists/:id        # Delete wishlist
GET    /api/wishlists/:id/items  # Get wishlist items
POST   /api/wishlists/:id/items  # Add item to wishlist
DELETE /api/wishlists/:id/items/:itemId # Remove item from wishlist
```

### Seller Routes
```
GET    /api/sellers              # Get all sellers
GET    /api/sellers/:id          # Get seller details
GET    /api/sellers/:id/products # Get products from seller
GET    /api/sellers/:id/reviews  # Get seller reviews
```

### Review Routes
```
POST   /api/reviews/product      # Submit product review
POST   /api/reviews/seller       # Submit seller review
GET    /api/reviews/user         # Get user's reviews
PUT    /api/reviews/:id          # Update review
DELETE /api/reviews/:id          # Delete review
POST   /api/reviews/:id/helpful  # Mark review as helpful
```

### User Account Routes
```
GET    /api/user/profile         # Get user profile
PUT    /api/user/profile         # Update user profile
GET    /api/user/addresses       # Get saved addresses
POST   /api/user/addresses       # Add new address
PUT    /api/user/addresses/:id   # Update address
DELETE /api/user/addresses/:id   # Delete address
GET    /api/user/payment-methods # Get saved payment methods
POST   /api/user/payment-methods # Add payment method
DELETE /api/user/payment-methods/:id # Remove payment method
```

### Recommendations Routes
```
GET    /api/recommendations/personalized # Get personalized recommendations
GET    /api/recommendations/trending     # Get trending items
GET    /api/recommendations/recently-viewed # Get recently viewed items
GET    /api/recommendations/frequently-bought # Items frequently bought together
```