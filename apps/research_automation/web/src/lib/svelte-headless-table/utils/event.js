export const isShiftClick = (event) => {
	if (!(event instanceof MouseEvent)) return false;
	return event.shiftKey;
};
