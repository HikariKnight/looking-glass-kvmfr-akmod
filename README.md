# Looking-Glass kvmfr kernel module akmod packaging for [Universal Blue](https://ublue.it) and Fedora Atomic Desktops
**NOTE: This is still a work in progress and might not be functional yet!**
RPM spec file for building the looking-glass kvmfr module as a kmod inside [copr](https://copr.fedorainfracloud.org/coprs/hikariknight/looking-glass-kvmfr/)
Primarily meant to be used when making Fedora Atomic Desktop images as the kernel module has to be included with the image.

For the Looking-Glass source code go to the [Looking Glass](https://github.com/gnif/LookingGlass) github repo which is not associated with me or Universal Blue

## Does this copr work for normal Fedora Workstation and Spins?
It is a normal akmods package so it should, however I do not test this.

## How do I use this in my image?
Run this script at some point inside your container file
NOTE: If there is a newer fedora release than `40`, please change `41` to be the new `rawhide` version number, this is `latest+1`

```bash
#!/bin/sh
set -oeux pipefail

ARCH="$(rpm -E '%_arch')"
KERNEL="$(rpm -q "${KERNEL_NAME:-kernel}" --queryformat '%{VERSION}-%{RELEASE}.%{ARCH}')"
RELEASE="$(rpm -E '%fedora')"

if [[ "${RELEASE}" -ge 41 ]]; then
    COPR_RELEASE="rawhide"
else
    COPR_RELEASE="${RELEASE}"
fi

wget "https://copr.fedorainfracloud.org/coprs/hikariknight/looking-glass-kvmfr/repo/fedora-${COPR_RELEASE}/hikariknight-looking-glass-kvmfr-fedora-${COPR_RELEASE}.repo" -O /etc/yum.repos.d/_copr_hikariknight-looking-glass-kvmfr.repo

### BUILD kvmfr (succeed or fail-fast with debug output)
rpm-ostree install \
    "akmod-kvmfr-*.fc${RELEASE}.${ARCH}"
akmods --force --kernels "${KERNEL}" --kmod kvmfr
modinfo "/usr/lib/modules/${KERNEL}/extra/kvmfr/kvmfr.ko.xz" > /dev/null \
|| (find /var/cache/akmods/kvmfr/ -name \*.log -print -exec cat {} \; && exit 1)

rm -f /etc/yum.repos.d/_copr_hikariknight-looking-glass-kvmfr.repo
```
