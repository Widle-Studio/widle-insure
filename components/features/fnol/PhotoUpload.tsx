import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Upload, X, Image as ImageIcon } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface PhotoUploadProps {
    onPhotosSelected: (files: File[]) => void;
}

export function PhotoUpload({ onPhotosSelected }: PhotoUploadProps) {
    const [photos, setPhotos] = useState<File[]>([]);
    const [previews, setPreviews] = useState<string[]>([]);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            const newFiles = Array.from(e.target.files);
            const updatedPhotos = [...photos, ...newFiles];
            setPhotos(updatedPhotos);
            onPhotosSelected(updatedPhotos);

            // Generate previews
            const newPreviews = newFiles.map(file => URL.createObjectURL(file));
            setPreviews([...previews, ...newPreviews]);
        }
    };

    const removePhoto = (index: number) => {
        const updatedPhotos = photos.filter((_, i) => i !== index);
        const updatedPreviews = previews.filter((_, i) => i !== index);

        // Revoke object URL to avoid memory leaks
        URL.revokeObjectURL(previews[index]);

        setPhotos(updatedPhotos);
        setPreviews(updatedPreviews);
        onPhotosSelected(updatedPhotos);
    };

    return (
        <div className="space-y-6">
            <div className="text-center space-y-2">
                <h3 className="text-lg font-medium">Upload Damage Photos</h3>
                <p className="text-sm text-muted-foreground">
                    Please upload clear photos of the damage. You can upload multiple images.
                </p>
            </div>

            <Card className="border-2 border-dashed border-muted-foreground/25 bg-muted/50 hover:bg-muted/80 transition-colors">
                <CardContent className="flex flex-col items-center justify-center p-10 space-y-4 text-center cursor-pointer" onClick={() => document.getElementById('photos')?.click()}>
                    <div className="p-4 rounded-full bg-background shadow-sm">
                        <Upload className="h-8 w-8 text-primary" />
                    </div>
                    <div className="space-y-1">
                        <p className="text-sm font-medium">Click to upload or drag and drop</p>
                        <p className="text-xs text-muted-foreground">SVG, PNG, JPG or GIF (max 5MB)</p>
                    </div>
                    <Input
                        id="photos"
                        type="file"
                        multiple
                        accept="image/*"
                        onChange={handleFileChange}
                        className="hidden"
                    />
                </CardContent>
            </Card>

            <div className="space-y-4">
                <AnimatePresence>
                    {previews.length > 0 && (
                        <motion.div
                            className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                        >
                            {previews.map((src, index) => (
                                <motion.div
                                    key={index}
                                    className="relative group aspect-video rounded-xl overflow-hidden shadow-sm border bg-background"
                                    initial={{ scale: 0.9, opacity: 0 }}
                                    animate={{ scale: 1, opacity: 1 }}
                                    exit={{ scale: 0, opacity: 0 }}
                                    transition={{ delay: index * 0.1 }}
                                >
                                    <img src={src} alt={`Preview ${index}`} className="h-full w-full object-cover transition-transform group-hover:scale-105" />
                                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                        <Button
                                            type="button"
                                            variant="destructive"
                                            size="icon"
                                            onClick={(e) => { e.stopPropagation(); removePhoto(index); }}
                                            className="h-8 w-8 rounded-full"
                                        >
                                            <X className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </motion.div>
                            ))}
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
