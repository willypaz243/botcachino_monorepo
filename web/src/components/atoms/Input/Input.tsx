import React from 'react';
import styles from './Input.module.css';

interface InputProps {
  id: string;
  label?: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
}

export const Input: React.FC<InputProps> = ({ 
  id,
  label,
  value,
  onChange,
  placeholder,
  disabled = false,
  error,
}) => {
  return (
    <div className={styles.inputContainer}>
      {label && (
        <label htmlFor={id} className={styles.inputLabel}>
          {label}
        </label>
      )}
      
      <input
        id={id}
        className={`${styles.input} ${error ? styles.inputError : ''}`}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        aria-invalid={error !== undefined}
        aria-describedby={error ? `${id}-error` : undefined}
      />
      
      {error && (
        <span id={`${id}-error`} className={styles.inputErrorText}>
          {error}
        </span>
      )}
    </div>
  );
};

export default Input;
