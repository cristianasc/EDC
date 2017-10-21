<xsl:stylesheet version="2.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 <xsl:output omit-xml-declaration="yes" indent="yes"/>
    <xsl:param name="pReplacement" select="'Something Different'"/>

     <xsl:template match="@*|node()">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:template>

     <xsl:template match="rss/channel/item/guid/text()">
         <xsl:value-of select="translate(.,'https://uaonline.ua.pt/pub/detail.asp?c=','')"/>
     </xsl:template>

</xsl:stylesheet>