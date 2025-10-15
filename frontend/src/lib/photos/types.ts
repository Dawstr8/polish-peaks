import { Peak } from "@/lib/peaks/types";

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
  peak?: Peak;
}

export interface SummitPhotoCreate {
  captured_at?: string;
  latitude?: number;
  longitude?: number;
  altitude?: number;
  peak_id?: number;
  distance_to_peak?: number;
}
