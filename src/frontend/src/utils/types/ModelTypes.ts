export interface AlbumImages {
  large: string;
  medium: string;
  small: string;
}

export interface AlbumData {
  id: string;
  name: string;
  images: AlbumImages;
}

export interface ArtistData {
  id: string;
  name: string;
}


export interface TrackType {
  id: string;
  name: string;
  artist_data: [ArtistData];
  album_data: AlbumData; 
  duration_ms: number;
  position?: number;
  explicit: boolean;
  popularity?: string;
  added_at?: string;
  added_by?: string;
  is_local: boolean;
  url: string;
  onClick?: Function;
  isSelected: boolean;
}

export interface PlaylistType {
  id: string;
  name: string;
  coverURL: string;
  ownerID: string;
  ownerName: string;
  description?: string;
  length: number;
  url?: string;
  isPublic: boolean;
  isCollaborative: boolean;
  tracks?: TrackType[];
  isSelected: boolean;
}

export interface AlbumType {
  artists: ArtistData[];
  genres: [];
  id: string;
  name: string;
  images: AlbumImages;
  release_date: string;
  total_tracks: number;
  url: string;
  type: string;
  tracks?: TrackType[];
}

export interface ArtistType {
  followers: number;
  genres: [];
  id: string;
  images: AlbumImages;
  name: string;
  url: string;
  popularity: number;
}

export interface LibraryData {
  playlists: PlaylistType[];
  albums: AlbumType[];
  artists: ArtistType[];
  tracks: TrackType[];
}
