from unittest.mock import AsyncMock


async def test_unit_download_version_no_remote_versions_no_matching_version(mock_hub, hub, capfd):
    """
    SCENARIO #1:
    - No remote versions
    - The specified version to download does not match any remote versions
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.download_version = hub.saltenv.ops.download_version

    # Mock the fill_remote_version_list function so it does nothing
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = AsyncMock()

    # Set REMOTE_VERSIONS as an empty dict
    mock_hub.saltenv.ops.REMOTE_VERSIONS = {}

    # Call download_version
    version_to_download = "3001"
    actual_ret = await mock_hub.saltenv.ops.download_version(version_to_download)
    actual_ret == False

    # Check that the expected output was printed (in this case nothing should be printed)
    actual_stdout, err = capfd.readouterr()
    expected_stdout = ""
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.saltenv.ops.fill_remote_version_list.assert_called_once_with()


async def test_unit_use_version_remote_versions_no_matching_version(mock_hub, hub, capfd):
    """
    SCENARIO #2:
    - There are already remote versions
    - The specified version to download does not match any of the remote versions
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.download_version = hub.saltenv.ops.download_version

    # Mock the fill_remote_version_list function so it does nothing
    mock_hub.saltenv.ops.fill_remote_version_list.return_value = AsyncMock()

    # Add mock data to REMOTE_VERSIONS
    mock_hub.saltenv.ops.REMOTE_VERSIONS = {
        "3003.3": "3003.3-1",
        "3003": "3003",
        "3004": "3004-1",
        "3004rc1": "3004rc1-1",
        "latest": "latest",
    }

    # Call download_version
    version_to_download = "3001"
    actual_ret = await mock_hub.saltenv.ops.download_version(version_to_download)
    actual_ret == False

    # Check that the expected output was printed (in this case nothing should be printed)
    actual_stdout, err = capfd.readouterr()
    expected_stdout = ""
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    assert not mock_hub.saltenv.ops.fill_remote_version_list.called


"""
async def download_version(hub, version, **kwargs):
    '''
    This is the entrypoint for the async code in your project
    '''
    ret = False
    ctx = SimpleNamespace(acct={})
    if not hub.saltenv.ops.REMOTE_VERSIONS:
        await hub.saltenv.ops.fill_remote_version_list()

    if version in hub.saltenv.ops.REMOTE_VERSIONS:
        file_list = await hub.exec.request.raw.get(
            ctx,
            url=f"{hub.OPT.saltenv.repo_url}/{hub.saltenv.ops.REMOTE_VERSIONS[version]}",
        )
        soup = BeautifulSoup(file_list["ret"], "html.parser")
        links = [
            node["href"]
            for node in soup.find_all("a")
            if node.get("href") and not node["href"].endswith("/") and node["href"] != "../"
        ]

        arch = os.uname().machine
        if arch == "x86_64":
            arch = "amd64"

        pkg_name = ""
        # TODO: verify download with SHA/GPG
        for link in links:
            if arch in link and sys.platform in link:
                pkg_name = link

        if pkg_name:
            outfile = Path(hub.OPT.saltenv.saltenv_dir) / "downloads" / pkg_name
            outfile.parent.mkdir(parents=True, exist_ok=True)
            versions_dir = Path(hub.OPT.saltenv.saltenv_dir) / "versions"
            versions_dir.mkdir(parents=True, exist_ok=True)
            salt_bin_in = versions_dir / "salt"
            salt_bin_out = versions_dir / f"salt-{version}"

            download_url = "/".join(
                [
                    hub.OPT.saltenv.repo_url,
                    hub.saltenv.ops.REMOTE_VERSIONS[version],
                    pkg_name,
                ]
            )

            pkg = {}
            if not outfile.exists():
                pkg = await hub.exec.request.raw.get(
                    ctx,
                    url=download_url,
                )
                async with aiofiles.open(outfile, "wb") as ofile:
                    await ofile.write(pkg["ret"])

            if (outfile.exists() and not salt_bin_out.exists()) or (pkg and pkg["status"] == 200):
                filemimetype = mimetypes.guess_type(str(outfile))

                if (
                    filemimetype and filemimetype[0] == "application/zip"
                ) or outfile.suffix == ".zip":
                    print("Processing zip file...")
                    if zipfile.is_zipfile(outfile):
                        zip_source = zipfile.ZipFile(outfile)
                        zip_source.extractall(versions_dir)
                        if salt_bin_in.exists():
                            salt_bin_in.rename(salt_bin_out)
                        ret = salt_bin_out.exists()
                    else:
                        print(f"ERROR: Unable to extract {outfile}")
                elif filemimetype == ("application/x-tar", "gzip") or str(outfile).endswith(
                    ".tar.gz"
                ):
                    print("Processing tarball...")
                    if tarfile.is_tarfile(outfile):
                        with tarfile.open(outfile) as tar_source:
                            tar_source.extractall(versions_dir)
                        if salt_bin_in.exists():
                            salt_bin_in.rename(salt_bin_out)
                        ret = salt_bin_out.exists()
                    else:
                        print(f"ERROR: Unable to extract {outfile}")
                else:
                    print(f"ERROR: Unknown file type for download {outfile}: {filemimetype}")
    return ret
"""
