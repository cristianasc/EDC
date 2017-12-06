<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:html="http://www.w3.org/1999/xhtml"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                xmlns:foaf="http://xmlns.com/foaf/spec/"
                xmlns:spot="http://artists.org/pred/">

    <xsl:template match="/">
    <rdf:RDF>
        <xsl:apply-templates/>
    </rdf:RDF>
    </xsl:template>


    <xsl:template match="items">
            <xsl:variable name="items"><xsl:value-of select="id"/></xsl:variable>
            <rdf:Description rdf:about="http://www.artists.com/items/{$items}">
                <foaf:name_artist><xsl:value-of select="name"/></foaf:name_artist>
                <spot:followers><xsl:value-of select="followers/total"/></spot:followers>
                <spot:external_urls><xsl:value-of select="external_urls/spotify"/></spot:external_urls>
                <spot:id><xsl:value-of select="id"/></spot:id>
                <spot:href><xsl:value-of select="href"/></spot:href>


                <xsl:for-each select="genres">
                    <spot:genres>
                        <rdf:Description rdf:about="http://www.artists.com/genres/{.}">
                            <foaf:name><xsl:value-of select="."/></foaf:name>
                        </rdf:Description>
                    </spot:genres>
                </xsl:for-each>

                <xsl:for-each select="images">
                    <xsl:variable name="size"><xsl:value-of select="width"/></xsl:variable>
                    <spot:image>
                        <rdf:Description rdf:about="http://www.artists.com/image/{$items}/{$size}">
                            <foaf:url><xsl:value-of select="url"/></foaf:url>
                            <spot:width><xsl:value-of select="width"/></spot:width>
                            <spot:height><xsl:value-of select="height"/></spot:height>
                        </rdf:Description>
                    </spot:image>
                </xsl:for-each>
            </rdf:Description>
    </xsl:template>
</xsl:stylesheet>