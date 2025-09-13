// deviceDetection.ts - Device detection utilities for audio service

export interface DeviceInfo {
  isMobile: boolean;
  deviceType: '📱 MOBILE' | '🖥️ DESKTOP';
}

/**
 * Detect if the current device is mobile
 */
export function detectMobile(): boolean {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
         ('ontouchstart' in window) ||
         (navigator.maxTouchPoints > 0);
}

/**
 * Get device information with formatted labels
 */
export function getDeviceInfo(): DeviceInfo {
  const isMobile = detectMobile();
  return {
    isMobile,
    deviceType: isMobile ? '📱 MOBILE' : '🖥️ DESKTOP'
  };
}