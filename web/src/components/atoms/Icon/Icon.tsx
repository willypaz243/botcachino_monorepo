import React from 'react';
import { Check, X } from 'lucide-react';
import styles from './Icon.module.css';

type IconName = 'check' | 'x';

interface IconProps {
  name: IconName;
  size?: number;
  className?: string;
}

export const Icon: React.FC<IconProps> = ({ name, size = 16, className }) => {
  const icons: Record<IconName, React.ReactNode> = {
    check: <Check size={size} />,
    x: <X size={size} />,
  };

  return (
    <span className={`${styles.iconContainer} ${className || ''}`}>
      {icons[name] || null}
    </span>
  );
};

export default Icon;
