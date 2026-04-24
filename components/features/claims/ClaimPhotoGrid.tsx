import { API_URL } from "@/lib/api-client";

interface Photo {
  id: string;
  photo_url: string;
}

interface ClaimPhotoGridProps {
  photos: Photo[];
}

export function ClaimPhotoGrid({ photos }: ClaimPhotoGridProps) {
  if (!photos || photos.length === 0) return null;

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold">Analyzed Photos</h3>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {photos.map((photo) => (
          <div
            key={photo.id}
            className="relative aspect-video rounded-lg overflow-hidden border shadow-sm"
          >
            <img
              src={`${API_URL}${photo.photo_url}`}
              alt="Damage"
              className="object-cover w-full h-full"
            />
          </div>
        ))}
      </div>
    </div>
  );
}
