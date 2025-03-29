import camelcaseKeys from 'camelcase-keys';
import snakecaseKeys from 'snakecase-keys';

/**
 * Converts an object's keys from snake_case to camelCase
 * @param obj - The object with snake_case keys
 * @returns A new object with all keys converted to camelCase
 */
export function convertObjectKeysToCamel<T = any>(obj: Record<string, any>): T {
  return camelcaseKeys(obj, { deep: true }) as T;
}

/**
 * Converts an object's keys from camelCase to snake_case
 * @param obj - The object with camelCase keys
 * @returns A new object with all keys converted to snake_case
 */
export function convertObjectKeysToSnake<T = any>(obj: Record<string, any>): T {
  return snakecaseKeys(obj, { deep: true }) as T;
}

// For individual string conversions (if needed)
export function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

export function camelToSnake(str: string): string {
  return str.replace(/([A-Z])/g, '_$1').toLowerCase();
} 