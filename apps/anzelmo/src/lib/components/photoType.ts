import type { PhotoData } from './photoDatum';

export type PhotoType = {
	id: number;
	album: string;
	path: string;
	label: string;
	price: string;
};

export function newPhoto(photoData: PhotoData): PhotoType {
	return {
		id: Math.random() * 1000,
		album: photoData.album,
		path: photoData.path,
		label: photoData.label,
		price: photoData.price
	};
}
