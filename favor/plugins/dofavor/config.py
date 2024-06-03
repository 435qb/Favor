from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    people : str = '侯刘唐段'
    filename : str = 'Data.dat'