export function formatLatLong(value: number | null | undefined): number | null {
  if (typeof value !== 'number' || isNaN(value)) {
    return null; 
  }

  if (Math.abs(value) >= 1000) {
    return null; 
  }
  return parseFloat(value.toFixed(6));
}


