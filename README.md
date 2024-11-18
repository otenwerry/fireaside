# fireaside

This is code I wrote while doing a short winter internship for Fire Aside (fireaside.com).
Their ChipperDay program sends chipper trucks to chip up flammable materials at people's
homes and take them to the dump, to protect these homes from wildfire risk. 

In addition to reducing wildfire risk by encouraging homeowners to clean up their wildfire
fuel who otherwise wouldn't have taken action, this program saves gas emissions for 
those who would have driven their fuel to the dump themselves, because the chipper truck
takes fewer trips for the same amount of waste.

This code takes in a file containing homes served by the chipper program, a file containing
nearby dumps, and the percent of homeowners who would have driven to the dump themselves
without the program. It uses the Google Distance Matrix API to compute how far the truck
drove and how far the homeowners would have driven, then computes gas emission savings.
The motivation was to have concrete numbers to use to apply for energy efficienc grants.
