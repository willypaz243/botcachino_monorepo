/* ============================================
   COMPONENT TYPES - Tipos para componentes UI
   ============================================ */

import React from 'react';

export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export interface AvatarProps {
  icon?: string;
  image?: string;
  alt?: string;
  size?: 'sm' | 'md' | 'lg';
}

export interface BadgeProps {
  variant?: 'primary' | 'secondary' | 'accent';
  children: React.ReactNode;
}

export interface ChatHeaderProps {
  title: string;
  status: 'online' | 'offline' | 'typing';
}
