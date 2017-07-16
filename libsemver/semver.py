"""
SemVer management class
"""

from .semver_core import SemVerCore

class SemVer(SemVerCore):
    def format(self, format_string):
        """
        Format the SemVer object using the following format specifiers
        {major}, {minor}, {patch}, {prerelease}, {build_metadata}
        """

        prerelease_formatted = ''
        if self.prerelease is not None:
            prerelease_formatted = '-' + \
                ''.join([str(p) for p in self.prerelease])

        build_metadata_formatted = ''
        if self.build_metadata is not None:
            build_metadata_formatted = '+' + ''.join(self.build_metadata)

        return format_string.format(
            major=self.major,
            minor=self.minor,
            patch=self.patch,
            prerelease=prerelease_formatted,
            build_metadata=build_metadata_formatted)


    def bump_major(self):
        """
        Bump the major number by 1 and reset the minor and patch versions
        """
        self._major += 1
        self._minor = 0
        self._patch = 0


    def bump_minor(self):
        """
        Bump the minor number by 1 and reset the patch version
        """
        self._minor += 1
        self._patch = 0


    def bump_patch(self):
        """
        Bump the patch number by 1
        """
        self._patch += 1


