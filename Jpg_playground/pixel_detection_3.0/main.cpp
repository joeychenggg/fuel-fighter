#include <iostream>
#include <vector>


// FROM: /LIDAR_MAP
std::vector<int> resolution {696, 502}; 
double meterPerPix = 0.05;

// FROM: .YAML FILE
std::vector<double> slamMapOrigin {-14.55, -10.60}; // LOWER-LEFT PIXEL OF THE MAP WITH REGARD TO THE MAP LINK (LIDAR ORIGO/START POSITION OF THE CAR)

// FROM: /ODOM
std::vector<double> start {0.00, -15.00}; // WITH REGARD TO THE ODOM-LINK
std::vector<double> stop {5.62, -15.00};

double jpgWidthInMeters() {
	return meterPerPix * resolution.at(0); 
}

double jpgHeightInMeters() {
	return meterPerPix * resolution.at(1); 
}



double xAxisMax() { // WITH REGARD TO THE MAP-LINK
	return (slamMapOrigin.at(0) + jpgWidthInMeters());
}
double yAxisMax() {
	return (slamMapOrigin.at(0) + jpgHeightInMeters());
}


int jpgStartPosX() {
	return int((-1 * slamMapOrigin.at(0) / meterPerPix) + 0.5); // ROUND (RIGHT NOW I'M CASTING TO INT)
}

int jpgStartPosY() {
	return int(((jpgHeightInMeters() + slamMapOrigin.at(1)) / meterPerPix) + 0.5); // ROUND
}

int main() {
	std::cout << jpgStartPosX() << std::endl;
	std::cout << jpgStartPosY() << std::endl;

	return 0;

}

// GJØR OM PUNKTENE FRA PIX DETECTION TIL PUNKTER IRL (MAO I FORHOLD TIL MAP-LINKEN)
// PRØVE Å KJØRE ALT FRA SCRATCH
// STARTE I EN SVING, SE HVORDAN DET GÅR

