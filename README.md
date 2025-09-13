# Chess Puzzle Platform V2 🏆

[![Deploy Backend](https://github.com/ChrisColeTech/chessboard-vanilla-v2/actions/workflows/deploy-backend.yml/badge.svg)](https://github.com/ChrisColeTech/chessboard-vanilla-v2/actions/workflows/deploy-backend.yml)

A modern full-stack chess puzzle platform built with TypeScript, PostgreSQL, and React. Features over 32,000 chess puzzles with AI analysis, user progression tracking, and comprehensive learning paths.

## 🚀 Live Demo

**Production**: https://chessboard-backend-v2-production.up.railway.app  
**API Health**: https://chessboard-backend-v2-production.up.railway.app/health  

## ✨ Features

### Core Functionality
- 🧩 **32,615+ Chess Puzzles** from Lichess database
- 🎯 **Adaptive Difficulty** based on user rating (800-3000+)
- 🤖 **AI Analysis** with move suggestions and explanations
- 📊 **Progress Tracking** with detailed statistics
- 🏆 **Achievement System** with unlockable content

### Learning & Improvement
- 📚 **Structured Learning Paths** for skill development
- 🎓 **Interactive Tutorials** covering chess fundamentals
- 📈 **Performance Analytics** with rating progression
- 🔍 **Opening Explorer** with theory and practice
- 📝 **Game Review** with mistake analysis

### User Experience
- 🌓 **Dark/Light Theme** toggle
- 📱 **Responsive Design** for all devices
- ⚡ **Real-time Updates** with optimistic UI
- 🔄 **Offline Support** for puzzle solving
- 🎨 **Customizable Board** themes and pieces

## 🛠 Technology Stack

### Backend
- **Runtime**: Node.js 18+ with TypeScript
- **Framework**: Express.js with professional MVC architecture
- **Database**: PostgreSQL with connection pooling
- **Authentication**: JWT with secure sessions
- **API**: RESTful endpoints with comprehensive validation

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development
- **Styling**: Modern CSS with responsive design
- **State Management**: Context API with useReducer
- **Chess Engine**: Custom move validation and analysis

### Infrastructure
- **Deployment**: Railway for full-stack hosting
- **Database**: Supabase PostgreSQL (free tier)
- **Monitoring**: Built-in health checks and logging
- **CI/CD**: Git-based deployment with automated builds

## 📁 Project Structure

```
chessboard-vanilla-v2/
├── package.json                 # Root scripts for deployment
├── .github/workflows/           # CI/CD automation
├── backend-v2/                  # TypeScript Express server
│   ├── src/
│   │   ├── app.ts              # Main application server
│   │   ├── utils/database.ts   # PostgreSQL connection
│   │   ├── services/           # Business logic (6 services)
│   │   ├── routes/             # API endpoints (33 endpoints)
│   │   ├── models/             # TypeScript interfaces
│   │   └── middleware/         # Auth, validation, CORS
│   ├── dist/                   # Compiled JavaScript
│   └── package.json            # Backend dependencies
├── frontend/                    # React application
│   ├── app/src/                # React components
│   ├── dist/                   # Built production files
│   └── package.json            # Frontend dependencies
├── tools/                      # Development utilities
│   ├── backend_generator.py    # Code generation tool
│   └── backend_config.json     # API configuration
└── docs/                       # Technical documentation
```

## 🚦 Quick Start

### Prerequisites
- Node.js 18+ and npm
- PostgreSQL database (or use Supabase)
- Git for version control

### Development Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:USERNAME/chessboard-vanilla-v2.git
   cd chessboard-vanilla-v2
   ```

2. **Install dependencies**
   ```bash
   # Install root dependencies
   npm install
   
   # Install backend dependencies
   cd backend-v2 && npm install && cd ..
   
   # Install frontend dependencies
   cd frontend/app && npm install && cd ../..
   ```

3. **Environment Configuration**
   ```bash
   # Backend environment
   cp backend-v2/.env.example backend-v2/.env
   # Edit DATABASE_URL and JWT_SECRET
   
   # Frontend environment (if needed)
   cp frontend/app/.env.example frontend/app/.env.local
   ```

4. **Database Setup**
   ```bash
   # Using provided PostgreSQL connection
   cd backend-v2
   npm run db:migrate  # Run database migrations
   npm run db:seed     # Optional: seed with sample data
   ```

5. **Development Server**
   ```bash
   # Start both frontend and backend
   npm run dev
   
   # Or run separately:
   # Backend: cd backend-v2 && npm run dev
   # Frontend: cd frontend/app && npm run dev
   ```

6. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:3001/api
   - Health check: http://localhost:3001/api/health

## 🔧 API Endpoints

### Core Endpoints
```
GET    /api/health              # Health check
GET    /api/puzzles/next        # Get next puzzle
POST   /api/puzzles/:id/solve   # Submit solution
GET    /api/games               # User's games
POST   /api/games               # Create new game
GET    /api/users/profile       # User profile
PUT    /api/users/preferences   # Update preferences
GET    /api/stats/overview      # User statistics
```

### Full API Documentation
See [API Documentation](docs/api.md) for complete endpoint reference.

## 🏗 Development

### Code Generation
The project uses automated code generation for consistent API development:

```bash
# Generate new endpoint
cd tools
python backend_generator.py <endpoint_name>

# Available endpoints: users, puzzles, games, stats, learning, tutorials
```

### Running Tests
```bash
# Backend tests
cd backend-v2 && npm test

# Frontend tests
cd frontend/app && npm test

# Full test suite
npm run test:all
```

### Building for Production
```bash
# Build everything
npm run build

# Build components separately
npm run build:frontend
npm run build:backend
```

## 🚀 Deployment

### Railway Deployment (Recommended)

1. **Prepare the repository**
   ```bash
   git add . && git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy to Railway**
   - Connect your GitHub repository to Railway
   - Set environment variables in Railway dashboard
   - Deploy automatically triggers on main branch push

3. **Environment Variables**
   ```bash
   DATABASE_URL=postgresql://user:pass@host:5432/database
   JWT_SECRET=your-secret-key
   NODE_ENV=production
   PORT=3001
   ```

### Manual Deployment
See [Deployment Guide](docs/deployment.md) for detailed instructions.

## 🎯 Performance

### Database Optimization
- **Connection Pooling**: Efficient PostgreSQL connections
- **Indexed Queries**: Optimized puzzle lookups by rating/theme
- **Query Batching**: Reduced database round trips

### Frontend Performance
- **Code Splitting**: Lazy-loaded routes and components
- **Asset Optimization**: Compressed images and fonts
- **Caching Strategy**: Service worker for offline functionality

### Benchmarks
- **API Response Time**: <200ms average
- **Database Queries**: <50ms for puzzle retrieval
- **Frontend Load**: <2s initial page load
- **Lighthouse Score**: 90+ across all metrics

## 🔒 Security

- **Authentication**: JWT tokens with secure httpOnly cookies
- **Input Validation**: Comprehensive request validation
- **SQL Injection**: Parameterized queries throughout
- **CORS**: Properly configured for frontend domain
- **Environment**: Secure credential management

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Standards
- TypeScript with strict mode
- ESLint + Prettier configuration
- Comprehensive unit tests
- Professional commit messages

## 📊 Database Schema

The application uses PostgreSQL with 29 optimized tables:

### Core Tables
- `puzzles` (32,615 records) - Chess puzzles with solutions
- `users` - User accounts and preferences  
- `games` - Game records and analysis
- `user_progress` - Skill tracking and statistics

### Supporting Tables
- `puzzle_themes` - Tactical pattern categories
- `learning_paths` - Structured skill development
- `achievements` - Gamification and motivation
- `game_analysis` - AI-powered move evaluation

## 🎨 UI/UX Design

### Design Principles
- **Minimalist**: Clean, distraction-free interface
- **Accessible**: WCAG 2.1 AA compliance
- **Responsive**: Mobile-first design approach
- **Intuitive**: Clear navigation and feedback

### Visual Elements
- **Typography**: Modern, readable font stack
- **Colors**: Carefully chosen contrast ratios
- **Icons**: Consistent iconography system
- **Animations**: Subtle, purposeful transitions

## 📈 Analytics & Monitoring

### Application Monitoring
- Health check endpoints for uptime monitoring
- Performance metrics collection
- Error tracking and alerting
- User behavior analytics (privacy-focused)

### Database Monitoring
- Connection pool metrics
- Query performance tracking
- Storage usage monitoring
- Backup verification

## 🔮 Roadmap

### Version 2.1 (Q1 2024)
- [ ] Real-time multiplayer puzzles
- [ ] Advanced AI analysis with Stockfish integration
- [ ] Mobile app (React Native)
- [ ] Tournament system

### Version 2.2 (Q2 2024)
- [ ] Social features and communities
- [ ] Custom puzzle creation tools
- [ ] Advanced statistics dashboard
- [ ] Integration with chess.com/lichess APIs

### Version 3.0 (Q3 2024)
- [ ] Machine learning for personalized recommendations
- [ ] Advanced opening repertoire builder
- [ ] Video lesson integration
- [ ] Premium subscription features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Lichess** for providing the comprehensive puzzle database
- **Railway** for excellent deployment platform
- **Supabase** for reliable PostgreSQL hosting
- **Chess.js** community for chess programming resources
- **TypeScript** team for excellent developer experience

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/USERNAME/chessboard-vanilla-v2/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/USERNAME/chessboard-vanilla-v2/discussions)
- 📧 **Contact**: [your-email@example.com](mailto:your-email@example.com)
- 📚 **Documentation**: [docs/](docs/)

---

⭐ **Star this repository** if you find it helpful!

Built with ❤️ for chess enthusiasts worldwide.