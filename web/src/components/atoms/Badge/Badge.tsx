import React from 'react';
import type { BadgeProps } from '../../../types/component.types';
import styles from './Badge.module.css';

export const Badge: React.FC<BadgeProps> = ({ 
  variant = 'primary', 
  children 
}) => {
  return (
    <span className={`${styles.badge} ${styles[`badge--${variant}`]}`}>
      {children}
    </span>
  );
};

export default Badge;
