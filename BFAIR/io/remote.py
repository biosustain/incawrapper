"""Remote.

This module hosts functions to download remote data.
"""

__all__ = ["LOCAL_PATH", "remote_files", "fetch_remote"]

import json
import requests

from collections import namedtuple
from hashlib import md5
from pathlib import Path

from BFAIR.io._base import _BaseFactory
from BFAIR.io._path import static_path

LOCAL_PATH = Path.home() / "BFAIR"
LOCAL_PATH.mkdir(parents=True, exist_ok=True)

_FileInfo = namedtuple("FileInfo", ["url", "expected_checksum", "expected_size"])


class _Files(_BaseFactory):
    def __init__(self):
        super().__init__(self.get_file_info)
        with open(static_path("remote_files.txt"), "r") as file:
            self._dict = json.load(file)
        self._list = [*self._dict.keys()]

    def get_file_info(self, filename):
        return _FileInfo._make(self._dict[filename])


def fetch_remote(canonical_filename: str, destination: Path):
    """
    Downloads a remote file into destination path.

    Parameters
    ----------
    canonical_filename : str
        Canonical name of the file that should be retrieved.
    destination : Path
        Pathname to save the file to.

    Raises
    ------
    ValueError
        If an unsupported filename is given.

    See Also
    --------
    remote_files
    """
    file_info = remote_files[canonical_filename]
    if file_info is None:
        raise ValueError(
            f"Unexpected filename {canonical_filename}. Check the documentation to see which files can be downloaded."
        )
    with requests.get(file_info.url, stream=True) as request:
        request.raise_for_status()
        with open(destination, "wb") as file:
            for chunk in request.iter_content(chunk_size=8192):
                file.write(chunk)
    size, checksum = get_filesize(destination), get_checksum(destination)
    if checksum != file_info.expected_checksum or size != file_info.expected_size:
        raise IOError(f"The downloaded file `{destination}` is corrupted. Remove it and try re-downloading.")
    return destination


def get_checksum(pathname: Path, hash_function=md5) -> str:
    """
    Returns the checksum of a file.

    Parameters
    ----------
    pathname : Path
    hash_function : callable
        Hashing function used to calculate the checksum.

    Returns
    -------
    str
    """
    hash_ = hash_function()
    with open(pathname, "rb") as file:
        for buffer in iter(lambda: file.read(8192), b""):
            hash_.update(buffer)
    return hash_.hexdigest()


def get_filesize(pathname: Path) -> int:
    """
    Returns the size of a file in bytes.

    Parameters
    ----------
    pathname : Path

    Returns
    -------
    int
    """
    return pathname.stat().st_size


remote_files = _Files()
"""A factory class to fetch remote file information. Use indexing to access its members.

Example
-------
>>> dir(files)
['rules_hs.db', 'rules_nohs.db']

>>> file_info = files['rules_hs.db']
>>> file_info.url
'https://ndownloader.figshare.com/files/26690771'
"""
