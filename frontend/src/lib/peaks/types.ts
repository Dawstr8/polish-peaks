export interface Peak {
  id: number;
  name: string;
  elevation: number;
  latitude: number;
  longitude: number;
  range: string;
}

export interface PeakWithDistance {
  peak: Peak;
  distance: number;
}
