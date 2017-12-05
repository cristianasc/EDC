<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:html="http://www.w3.org/1999/xhtml"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                xmlns:foaf="http://xmlns.com/foaf/spec/"
                xmlns:spot="http://new-releases.org/pred/">

    <xsl:template match="/">
    <rdf:RDF>
        <xsl:apply-templates/>
    </rdf:RDF>
    </xsl:template>


    <xsl:template match="items">
            <xsl:variable name="items"><xsl:value-of select="id"/></xsl:variable>
            <rdf:Description rdf:about="http://www.new-releases.com/items/{$items}">
                <foaf:name_album><xsl:value-of select="name"/></foaf:name_album>
                <spot:album_type><xsl:value-of select="album_type"/></spot:album_type>
                <spot:external_urls><xsl:value-of select="external_urls/spotify"/></spot:external_urls>
                <spot:id><xsl:value-of select="id"/></spot:id>
                <spot:href><xsl:value-of select="href"/></spot:href>

                <xsl:for-each select="available_markets">
                    <spot:available_markets>
                        <rdf:Description rdf:about="http://www.new-releases.com/available_markets/{.}">
                            <foaf:name><xsl:value-of select="."/></foaf:name>
                        </rdf:Description>
                    </spot:available_markets>
                </xsl:for-each>

                <xsl:for-each select="artists">
                    <spot:artists>
                        <rdf:Description rdf:about="http://www.new-releases.com/artists">
                            <foaf:name><xsl:value-of select="name"/></foaf:name>
                            <spot:external_urls_spotify><xsl:value-of select="external_urls/spotify"/></spot:external_urls_spotify>
                            <spot:href><xsl:value-of select="href"/></spot:href>
                            <spot:id><xsl:value-of select="id"/></spot:id>
                            <spot:type><xsl:value-of select="type"/></spot:type>
                            <spot:uri><xsl:value-of select="uri"/></spot:uri>
                        </rdf:Description>
                    </spot:artists>
                </xsl:for-each>

                <xsl:for-each select="images">
                    <spot:image>
                        <rdf:Description rdf:about="http://www.new-releases.com/image/{$items}">
                            <foaf:url><xsl:value-of select="url"/></foaf:url>
                            <spot:width><xsl:value-of select="width"/></spot:width>
                            <spot:height><xsl:value-of select="height"/></spot:height>
                        </rdf:Description>
                    </spot:image>
                </xsl:for-each>

            </rdf:Description>
    </xsl:template>

</xsl:stylesheet>