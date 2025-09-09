/**
 * HeadlessUI Dialog-based action sheet - clean external state control
 * Uses HeadlessUI Dialog for proper accessibility, keyboard navigation, and focus management
 * Bottom sheet positioned above TabBar with backdrop dismissal
 */
import { Dialog, DialogPanel } from "@headlessui/react";
import { Settings, LogOut } from "lucide-react";
import { ActionItem } from "./ActionItem";
import type { ActionSheetProps } from "../../types/core/action-sheet.types";
import { useRef, useState } from "react";

export function ActionSheet({
  actions,
  onActionClick,
  onActionHover,
  onKeyDown,
  className,
  onClose,
  isOpen,
}: ActionSheetProps) {
  const panelRef = useRef<HTMLDivElement>(null);
  const [startY, setStartY] = useState(0);
  const [currentY, setCurrentY] = useState(0);
  const [isDragging, setIsDragging] = useState(false);

  const handleClose = () => {
    onClose?.();
  };

  const handleTouchStart = (e: React.TouchEvent) => {
    const touch = e.touches[0];
    setStartY(touch.clientY);
    setCurrentY(touch.clientY);
    setIsDragging(true);
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isDragging) return;
    const touch = e.touches[0];
    const deltaY = touch.clientY - startY;

    // Only allow downward movement
    if (deltaY > 0) {
      setCurrentY(touch.clientY);
      // Apply transform to create drag effect
      if (panelRef.current) {
        panelRef.current.style.transform = `translateY(${deltaY}px)`;
        panelRef.current.style.opacity = `${Math.max(0.5, 1 - deltaY / 200)}`;
      }
    }
  };

  const handleTouchEnd = () => {
    if (!isDragging) return;
    setIsDragging(false);

    const deltaY = currentY - startY;

    // If dragged down more than 100px, close the sheet
    if (deltaY > 100) {
      handleClose();
    } else {
      // Reset position
      if (panelRef.current) {
        panelRef.current.style.transform = "translateY(0px)";
        panelRef.current.style.opacity = "1";
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    onKeyDown?.(e);
    if (e.key === "Escape") {
      handleClose();
    }
  };

  return (
    <Dialog
      open={isOpen}
      onClose={handleClose}
      className={`relative z-50 ${className ?? ""}`}
    >
      {/* Responsive positioning: left on desktop, full width on mobile */}
      <div className="fixed bottom-[84px] left-0 right-0 md:left-0 md:right-auto md:w-80 md:bottom-[84px]">
        <DialogPanel
          ref={panelRef}
          className="w-full action-sheet md:rounded-none p-4 md:p-0 space-y-2 select-none"
          transition
          onKeyDown={handleKeyDown}
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
        >
          {/* Visual handle for bottom sheet feel - mobile only */}
          <div className="w-10 h-1 bg-white/40 rounded-full mx-auto mb-4 md:hidden" />

          <div className="space-y-1" role="menu" aria-label="Page actions">
            {actions.map((action) => (
              <ActionItem
                key={action.id}
                action={action}
                onSelect={() => {
                  onActionClick(action, handleClose);
                  handleClose();
                }}
                onHover={() => onActionHover?.(action.label)}
              />
            ))}
          </div>

          {/* Global Settings Button - appears on all pages */}
          {actions.length > 0 && (
            <div className="border-t border-white/10 my-2"></div>
          )}
          <ActionItem
            action={{
              id: "open-settings",
              label: "Settings",
              icon: Settings,
              variant: "secondary",
            }}
            onSelect={() => {
              onActionClick(
                {
                  id: "open-settings",
                  label: "Settings",
                  icon: Settings,
                  variant: "secondary",
                },
                handleClose
              );
              handleClose();
            }}
            onHover={() => onActionHover?.("Settings")}
          />
          
          {/* Logout Button */}
          <ActionItem
            action={{
              id: "logout",
              label: "Logout",
              icon: LogOut,
              variant: "destructive",
            }}
            onSelect={() => {
              onActionClick(
                {
                  id: "logout",
                  label: "Logout",
                  icon: LogOut,
                  variant: "destructive",
                },
                handleClose
              );
              handleClose();
            }}
            onHover={() => onActionHover?.("Logout")}
          />
        </DialogPanel>
      </div>
    </Dialog>
  );
}
