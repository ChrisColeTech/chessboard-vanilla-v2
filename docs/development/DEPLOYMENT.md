# Railway Deployment Guide 🚂

Complete guide for deploying the Chess Puzzle Platform V2 to Railway with full-stack configuration.

## 📋 Prerequisites

- [Railway Account](https://railway.app) (free tier available)
- [GitHub Account](https://github.com) with repository access
- [Supabase Account](https://supabase.com) for PostgreSQL database
- Environment variables configured

## 🚀 Quick Deployment Steps

### 1. Repository Setup
```bash
# Clone your repository
git clone git@github.com:USERNAME/chessboard-vanilla-v2.git
cd chessboard-vanilla-v2

# Ensure you're on main branch
git checkout main
git push origin main
```

### 2. Railway Project Creation

1. **Go to [Railway Dashboard](https://railway.app/dashboard)**
2. **Click "New Project" → "Deploy from GitHub repo"**
3. **Select your `chessboard-vanilla-v2` repository**
4. **Railway will automatically detect Node.js project**

### 3. Environment Configuration

In Railway Dashboard → Project → Variables, add:

```bash
# Required Variables
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-1-us-east-2.pooler.supabase.com:5432/postgres
NODE_ENV=production
JWT_SECRET=your-super-secure-random-string-here

# Optional Variables  
PORT=3001
CORS_ORIGINS=https://your-app.railway.app
ENABLE_TEST_DB_ENDPOINT=false
```

### 4. Database Setup (Supabase)

1. **Create Supabase Project** at [supabase.com](https://supabase.com)
2. **Get Connection String** from Project Settings → Database
3. **Use Connection Pooler URL** (IPv4 compatible):
   ```
   postgresql://postgres.xxxxx:[PASSWORD]@aws-1-us-east-2.pooler.supabase.com:5432/postgres
   ```
4. **Import Database Schema** (if you have existing data)

### 5. Deploy & Verify

1. **Automatic Deployment**: Railway deploys on git push to main
2. **Monitor Build Logs** in Railway dashboard
3. **Check Health Endpoint**: `https://your-app.railway.app/api/health`
4. **Test Frontend**: `https://your-app.railway.app/`

## 🏗 Build Process

Railway automatically runs these commands:

```json
{
  "build": "npm run build:frontend && npm run build:backend",
  "start": "cd backend && npm start"
}
```

### Build Steps:
1. **Frontend Build**: `cd frontend/app && npm install && npm run build`
2. **Backend Build**: `cd backend && npm install && npm run build`
3. **Static Serving**: Backend serves frontend from `frontend/app/dist`

## 🔧 Advanced Configuration

### Custom Domain Setup
```bash
# In Railway Dashboard → Settings → Domains
# Add custom domain: yourdomain.com
# Configure DNS CNAME record pointing to Railway
```

### Environment-Specific Deployments
```bash
# Create separate Railway services for:
# - Production (main branch)
# - Staging (develop branch)  
# - Review apps (feature branches)
```

### Database Migrations
```bash
# Add to Railway build process if needed
"build": "npm run build && npm run db:migrate"
```

## 📊 Monitoring & Maintenance

### Health Checks
- **Endpoint**: `/api/health`
- **Expected Response**: `{"success": true, "status": "healthy"}`
- **Railway Auto-Restart**: On health check failures

### Database Monitoring
- **Connection Pool**: Monitor active connections
- **Query Performance**: Check slow query log
- **Storage Usage**: Track database size growth

### Application Logs
```bash
# View logs in Railway Dashboard → Deployments → Logs
# Or use Railway CLI:
railway logs --tail
```

## 🐛 Troubleshooting

### Common Issues

#### Build Failures
```bash
# Issue: Frontend build fails
# Solution: Check Node.js version compatibility
"engines": {
  "node": "18.x",
  "npm": "9.x"
}
```

#### Database Connection Errors
```bash
# Issue: ENETUNREACH error
# Solution: Use Supabase Connection Pooler (IPv4):
DATABASE_URL=postgresql://...@aws-1-us-east-2.pooler.supabase.com:5432/postgres
```

#### Static File Serving Issues
```bash
# Issue: Frontend routes return 404
# Solution: Check app.ts fallback route:
app.get('*', (req, res) => {
  if (!req.path.startsWith('/api/')) {
    res.sendFile(path.join(frontendPath, 'index.html'));
  }
});
```

### Environment Variable Issues
```bash
# Issue: Variables not loading
# Solution: Restart Railway deployment after variable changes
# Variables are injected at runtime, not build time
```

## 🔒 Security Checklist

- [ ] **JWT_SECRET** is cryptographically strong (>32 characters)
- [ ] **DATABASE_URL** uses SSL connection
- [ ] **CORS_ORIGINS** is configured for production domain
- [ ] **NODE_ENV=production** is set
- [ ] **Sensitive data** is not logged in production
- [ ] **API rate limiting** is configured (if needed)

## 📈 Performance Optimization

### Frontend Optimizations
```bash
# Build optimizations already configured:
# - Vite bundling with tree shaking
# - Asset compression
# - Code splitting
```

### Backend Optimizations
```bash
# Database connection pooling configured
# Static file serving via Express
# Compressed responses with helmet middleware
```

### Railway-Specific Optimizations
```bash
# Use Railway's built-in CDN
# Configure appropriate server regions
# Monitor resource usage in Railway dashboard
```

## 🔄 CI/CD Workflow

GitHub Actions automatically:
1. **Runs Tests** on every PR/push
2. **Builds Application** to verify compilation
3. **Deploys to Railway** on main branch push
4. **Health Check** post-deployment

### Manual Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link [project-id]
railway up
```

## 💰 Cost Considerations

### Railway Pricing
- **Free Tier**: $5 monthly credit
- **Usage-Based**: CPU, memory, network
- **Typical App Cost**: $1-3/month for development

### Supabase Pricing
- **Free Tier**: 500MB database, 2GB bandwidth
- **Typical Usage**: Well within free limits for development

### Monitoring Costs
```bash
# Check Railway usage dashboard
# Monitor database storage growth
# Optimize queries to reduce CPU usage
```

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Supabase Documentation](https://supabase.com/docs)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [PostgreSQL Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)

## 🆘 Support

### Getting Help
- **Railway Support**: [Railway Discord](https://discord.gg/railway)
- **Supabase Support**: [Supabase Discord](https://discord.supabase.com/)
- **Project Issues**: [GitHub Issues](https://github.com/USERNAME/chessboard-vanilla-v2/issues)

### Community Resources
- **Railway Templates**: [railway.app/templates](https://railway.app/templates)
- **Deployment Examples**: [Railway Examples](https://github.com/railwayapp/examples)

---

🎉 **Congratulations!** Your chess puzzle platform is now deployed and accessible worldwide!

🔗 **Next Steps**: Set up monitoring, configure custom domain, and enjoy your deployed application.