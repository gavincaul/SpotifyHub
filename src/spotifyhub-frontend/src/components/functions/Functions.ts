// Central registry for page-specific Functions definitions
// Each exported function returns groups for that page
// Types intentionally permissive to interop with JS pages.

export type FnField = {
  name: string;
  label: string;
  type?: "text" | "number" | "toggle" | "select" | "source";
  placeholder?: string;
  options?: Array<{ label: string; value: any }>;
  defaultValue?: any;
  accept?: 'playlist' | 'track' | 'album' | 'any';
};

export type FnItem = {
  id: string;
  title: string;
  description?: string;
  fields?: FnField[];
  run: (values: Record<string, any>) => Promise<any> | any;
  danger?: boolean;
  disabled?: boolean;
  ctaLabel?: string;
};

export type FnGroup = { group: string; items: FnItem[] };

// Central registry for page-specific Functions definitions
// Each exported function returns groups for that page
// Types intentionally permissive to interop with JS pages.

// Playlists page definitions
export function Playlists(): FnGroup[] {
  const createPlaylist: FnItem = {
    id: "create-playlist",
    title: "Create Playlist",
    description: "Create a new playlist in your account.",
    fields: [
      { name: "name", label: "Name", type: "text", placeholder: "My New Playlist" },
      { name: "public", label: "Public", type: "toggle", defaultValue: true },
      { name: "collab", label: "Collaborative", type: "toggle", defaultValue: false },
    ],
    run: async (values) => {
      // TODO: integrate with Spotify API
      await new Promise((r) => setTimeout(r, 500));
      return { id: "pl_" + Math.random().toString(36).slice(2, 8), ...values };
    },
    ctaLabel: "Create",
  };

  const mergePlaylists: FnItem = {
    id: "merge-playlists",
    title: "Merge Playlists",
    description: "Combine two playlists using a strategy.",
    fields: [
      { 
        name: "sourceA", 
        label: "Source A", 
        type: "source", 
        placeholder: "Drop Playlist A here",
        accept: "playlist"
      },
      { 
        name: "sourceB", 
        label: "Source B", 
        type: "source", 
        placeholder: "Drop Playlist B here",
        accept: "playlist"
      },
      {
        name: "strategy",
        label: "Strategy",
        type: "select",
        options: [
          { label: "Union (A ∪ B)", value: "union" },
          { label: "Intersection (A ∩ B)", value: "intersect" },
          { label: "Difference (A − B)", value: "diff" },
        ],
        defaultValue: "union",
      },
    ],
    run: async (values) => {
      await new Promise((r) => setTimeout(r, 700));
      return { merged: true, count: Math.floor(Math.random() * 200) + 20, ...values };
    },
    ctaLabel: "Merge",
  };

  const analyzeTracks: FnItem = {
    id: "analyze-tracks",
    title: "Analyze Tracks",
    description: "Run a quick analysis on a playlist's tracks.",
    fields: [
      { 
        name: "playlist", 
        label: "Playlist", 
        type: "source", 
        placeholder: "Drop a playlist here",
        accept: "playlist"
      },
      {
        name: "metric",
        label: "Metric",
        type: "select",
        options: [
          { label: "Energy", value: "energy" },
          { label: "Danceability", value: "danceability" },
          { label: "Valence", value: "valence" },
        ],
        defaultValue: "energy",
      },
      { name: "topN", label: "Top N", type: "number", defaultValue: 10 },
    ],
    run: async (values) => {
      await new Promise((r) => setTimeout(r, 600));
      return { report: { metric: values.metric, topN: values.topN, avg: Math.random().toFixed(2) } };
    },
    ctaLabel: "Analyze",
  };

  return [
    { group: "Create/Manage", items: [createPlaylist, mergePlaylists] },
    { group: "Analysis", items: [analyzeTracks] },
  ];
}
