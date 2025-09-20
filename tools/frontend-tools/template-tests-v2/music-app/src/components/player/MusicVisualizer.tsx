import React, { useState, useEffect, useRef } from 'react';
import { usePlayer } from '../../stores/musicStore';

interface MusicVisualizerProps {
  type?: 'bars' | 'wave' | 'circle' | 'spectrum';
  className?: string;
  color?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const MusicVisualizer: React.FC<MusicVisualizerProps> = ({
  type = 'bars',
  className = '',
  color = 'primary',
  size = 'md',
}) => {
  const player = usePlayer();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const [audioData, setAudioData] = useState<number[]>([]);

  const sizeConfig = {
    sm: { width: 120, height: 40, barCount: 8 },
    md: { width: 200, height: 60, barCount: 16 },
    lg: { width: 300, height: 80, barCount: 24 },
  };

  const config = sizeConfig[size];

  // Simulate audio data since we don't have real audio analysis
  useEffect(() => {
    if (!player.isPlaying) {
      setAudioData(Array(config.barCount).fill(0.1));
      return;
    }

    const generateAudioData = () => {
      const data = Array(config.barCount).fill(0).map((_, index) => {
        // Simulate frequency data with some rhythm patterns
        const baseFreq = Math.sin(Date.now() * 0.005 + index * 0.5) * 0.3 + 0.4;
        const randomVariation = Math.random() * 0.3;
        const rhythmPattern = Math.sin(Date.now() * 0.01) * 0.2;
        
        return Math.max(0.1, Math.min(1, baseFreq + randomVariation + rhythmPattern));
      });
      
      setAudioData(data);
    };

    const interval = setInterval(generateAudioData, 50);
    return () => clearInterval(interval);
  }, [player.isPlaying, config.barCount]);

  // Canvas rendering
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (type === 'bars') {
        renderBars(ctx, canvas);
      } else if (type === 'wave') {
        renderWave(ctx, canvas);
      } else if (type === 'circle') {
        renderCircle(ctx, canvas);
      } else if (type === 'spectrum') {
        renderSpectrum(ctx, canvas);
      }

      if (player.isPlaying) {
        animationRef.current = requestAnimationFrame(render);
      }
    };

    render();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [audioData, player.isPlaying, type]);

  const renderBars = (ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement) => {
    const barWidth = canvas.width / audioData.length;
    const gradient = ctx.createLinearGradient(0, canvas.height, 0, 0);
    gradient.addColorStop(0, 'rgba(99, 102, 241, 0.8)');
    gradient.addColorStop(0.5, 'rgba(139, 92, 246, 0.9)');
    gradient.addColorStop(1, 'rgba(219, 39, 119, 1)');

    audioData.forEach((value, index) => {
      const barHeight = value * canvas.height * 0.8;
      const x = index * barWidth;
      const y = canvas.height - barHeight;

      ctx.fillStyle = gradient;
      ctx.fillRect(x + 1, y, barWidth - 2, barHeight);
      
      // Add glow effect
      ctx.shadowColor = 'rgba(139, 92, 246, 0.5)';
      ctx.shadowBlur = 4;
      ctx.fillRect(x + 1, y, barWidth - 2, barHeight);
      ctx.shadowBlur = 0;
    });
  };

  const renderWave = (ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement) => {
    ctx.strokeStyle = 'rgba(139, 92, 246, 0.8)';
    ctx.lineWidth = 2;
    ctx.beginPath();

    const stepX = canvas.width / (audioData.length - 1);
    
    audioData.forEach((value, index) => {
      const x = index * stepX;
      const y = canvas.height / 2 + (value - 0.5) * canvas.height * 0.6;
      
      if (index === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });

    ctx.stroke();
    
    // Add glow
    ctx.strokeStyle = 'rgba(139, 92, 246, 0.3)';
    ctx.lineWidth = 6;
    ctx.stroke();
  };

  const renderCircle = (ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement) => {
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const baseRadius = Math.min(canvas.width, canvas.height) * 0.2;

    audioData.forEach((value, index) => {
      const angle = (index / audioData.length) * Math.PI * 2;
      const radius = baseRadius + value * baseRadius;
      
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      
      const gradient = ctx.createRadialGradient(x, y, 0, x, y, 5);
      gradient.addColorStop(0, 'rgba(139, 92, 246, 1)');
      gradient.addColorStop(1, 'rgba(139, 92, 246, 0)');
      
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(x, y, 3, 0, Math.PI * 2);
      ctx.fill();
    });
  };

  const renderSpectrum = (ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement) => {
    const barWidth = canvas.width / audioData.length;
    
    audioData.forEach((value, index) => {
      const hue = (index / audioData.length) * 360;
      const barHeight = value * canvas.height;
      
      ctx.fillStyle = `hsla(${hue}, 70%, 60%, 0.8)`;
      ctx.fillRect(index * barWidth, canvas.height - barHeight, barWidth - 1, barHeight);
      
      // Add top glow
      ctx.fillStyle = `hsla(${hue}, 70%, 80%, 0.6)`;
      ctx.fillRect(index * barWidth, canvas.height - barHeight, barWidth - 1, 3);
    });
  };

  if (!player.isPlaying && type !== 'bars') {
    return (
      <div className={`${className} flex items-center justify-center opacity-30`}>
        <div className="text-sm text-muted-foreground">Play music to see visualizer</div>
      </div>
    );
  }

  return (
    <div className={`${className} relative`}>
      <canvas
        ref={canvasRef}
        width={config.width}
        height={config.height}
        className="w-full h-full"
        style={{ 
          filter: player.isPlaying ? 'drop-shadow(0 0 8px rgba(139, 92, 246, 0.3))' : 'none',
          transition: 'filter 0.3s ease'
        }}
      />
      
      {!player.isPlaying && (
        <div className="absolute inset-0 bg-black/20 rounded flex items-center justify-center">
          <div className="text-xs text-white/60">Paused</div>
        </div>
      )}
    </div>
  );
};