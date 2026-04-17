import React from 'react';
import type { AvatarProps } from '../../../types/component.types';
import styles from './Avatar.module.css';

export const Avatar: React.FC<AvatarProps> = ({ 
  icon, 
  image, 
  alt = 'Avatar',
  size = 'md' 
}) => {
  const avatarSizeClasses: Record<'sm' | 'md' | 'lg', string> = {
    sm: styles.avatarSm,
    md: styles.avatarMd,
    lg: styles.avatarLg,
  };

  return (
    <div className={`${styles.avatar} ${avatarSizeClasses[size]}`}>
      {image ? (
        <img src={image} alt={alt} />
      ) : icon ? (
        <span className={styles.avatarIcon}>{icon}</span>
      ) : null}
    </div>
  );
};

export default Avatar;
