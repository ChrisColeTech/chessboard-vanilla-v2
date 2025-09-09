import { Request, Response, NextFunction } from 'express';

export const validate = (schema: any) => {
  return (req: Request, res: Response, next: NextFunction) => {
    // Basic validation middleware - can be enhanced with joi, yup, etc.
    // For now, just pass through
    next();
  };
};