import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export interface AuthenticatedRequest extends Request {
  user?: {
    id: string;
    username: string;
    email: string;
  };
  userId?: string;
}

export const authenticate = (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
  console.log(`🔐 Auth middleware: Processing authentication for ${req.method} ${req.path}`);
  
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    console.log('❌ Auth middleware: No token provided');
    return res.status(401).json({ error: 'Access token required' });
  }

  console.log(`🔍 Auth middleware: Token found, length: ${token.length}`);

  jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key', (err: any, user: any) => {
    if (err) {
      console.log('❌ Auth middleware: Token verification failed:', err.message);
      return res.status(403).json({ error: 'Invalid token' });
    }
    
    console.log('✅ Auth middleware: Token verified successfully');
    console.log('🔍 Auth middleware: Decoded user object:', JSON.stringify(user, null, 2));
    console.log(`🔍 Auth middleware: User fields available: ${Object.keys(user).join(', ')}`);
    
    req.user = user;
    // FIX: Changed from user.userId to user.id to match JWT token creation
    req.userId = user.id;
    
    console.log(`✅ Auth middleware: Setting req.userId to: ${req.userId}`);
    console.log(`🔍 Auth middleware: req.user set to:`, JSON.stringify(req.user, null, 2));
    
    next();
  });
};

export const optionalAuth = (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
  console.log(`🔐 Optional auth middleware: Processing for ${req.method} ${req.path}`);
  
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    console.log('ℹ️  Optional auth middleware: No token provided, continuing without auth');
    return next();
  }

  console.log(`🔍 Optional auth middleware: Token found, length: ${token.length}`);

  jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key', (err: any, user: any) => {
    if (!err) {
      console.log('✅ Optional auth middleware: Token verified successfully');
      console.log('🔍 Optional auth middleware: Decoded user object:', JSON.stringify(user, null, 2));
      console.log(`🔍 Optional auth middleware: User fields available: ${Object.keys(user).join(', ')}`);
      
      req.user = user;
      // FIX: Changed from user.userId to user.id to match JWT token creation
      req.userId = user.id;
      
      console.log(`✅ Optional auth middleware: Setting req.userId to: ${req.userId}`);
      console.log(`🔍 Optional auth middleware: req.user set to:`, JSON.stringify(req.user, null, 2));
    } else {
      console.log('⚠️  Optional auth middleware: Token verification failed, continuing without auth:', err.message);
    }
    next();
  });
};