export interface SummitPhoto {
  id?: number;
  file_name: string;
  uploaded_at: string;
  captured_at?: string;
  latitude?: number;
  longitude?: number;
  altitude?: number;
  peak_id?: number;
  distance_to_peak?: number;
}

export interface SummitPhotoCreate {
  captured_at?: string;
  latitude?: number;
  longitude?: number;
  altitude?: number;
  peak_id?: number;
  distance_to_peak?: number;
}
