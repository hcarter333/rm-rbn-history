import netCDF4

def getattr(file):
    nc_file = netCDF4.Dataset(file)
    print("Global Attributes:")
    for attr in nc_file.ncattrs():
        print(f"  {attr}: {nc_file.getncattr(attr)}")


def getvars(file):
    nc_file = netCDF4.Dataset(file)
    print("\nVariables:")
    for var in nc_file.variables:
        print(f"  {var}:")
        print(f"    Dimensions: {nc_file.variables[var].dimensions}")
        print(f"    Data type: {nc_file.variables[var].dtype}")
        print(f"    Attributes:")
        for attr in nc_file.variables[var].ncattrs():
            print(f"      {attr}: {nc_file.variables[var].getncattr(attr)}")


