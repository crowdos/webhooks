#!/usr/bin/python
# -*- coding: utf-8 -*-

SERVICE_TEMPLATE = """
<services>
  <service name="git_dsc">
    <param name="url">@URL@</param>
    <param name="branch">@BRANCH@</param>
    <param name="revision">@REVISION@</param>
  </service>
</services>
"""

NEW_PACKAGE_TEMPLATE = """
<package name="@PACKAGE@" project="@PROJECT@">
  <title/>
  <description/>
</package>
"""

NEW_PROJECT_TEMPLATE = """
<project name="@NAME@">
  <title/>
  <description/>
  <person userid="Admin" role="maintainer"/>
  <person userid="obs" role="maintainer"/>
  <publish>
    <disable/>
  </publish>
  <debuginfo>
    <disable/>
  </debuginfo>
</project>
"""
