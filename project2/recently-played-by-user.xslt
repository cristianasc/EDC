<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:html="http://www.w3.org/1999/xhtml"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                xmlns:foaf="http://xmlns.com/foaf/spec/"
                xmlns:spot="http://recently-played-by-user.org/pred/">

    <xsl:template match="/">
    <rdf:RDF>
        <xsl:apply-templates/>
    </rdf:RDF>
    </xsl:template>

    <xsl:template match="item">
        <xsl:variable name="item"><xsl:value-of select="track/id"/></xsl:variable>
            <rdf:Description rdf:about="http://www.recently-played-by-user.com/item/{$item}">
                <foaf:played_at><xsl:value-of select="played_at"/></foaf:played_at>

                <xsl:for-each select="track">
                    <spot:track>
                        <rdf:Description rdf:about="http://www.recently-played-by-user.com/track/{$item}">
                            <foaf:name><xsl:value-of select="name"/></foaf:name>
                            <spot:type><xsl:value-of select="type"/></spot:type>
                            <spot:external_urls><xsl:value-of select="external_urls/spotify"/></spot:external_urls>
                            <spot:id><xsl:value-of select="id"/></spot:id>
                            <spot:href><xsl:value-of select="href"/></spot:href>
                            <spot:disc_number><xsl:value-of select="disc_number"/></spot:disc_number>
                            <spot:popularity><xsl:value-of select="popularity"/></spot:popularity>
                            <spot:preview_url><xsl:value-of select="preview_url"/></spot:preview_url>
                            <spot:track_number><xsl:value-of select="track_number"/></spot:track_number>
                        </rdf:Description>
                    </spot:track>
                </xsl:for-each>

                <xsl:for-each select="track/artists/item">
                    <xsl:variable name="id"><xsl:value-of select="id"/></xsl:variable>
                    <spot:artists>
                        <rdf:Description rdf:about="http://www.recently-played-by-user.com/artists/{$item}/{$id}">
                            <foaf:name><xsl:value-of select="name"/></foaf:name>
                            <spot:external_urls_spotify><xsl:value-of select="external_urls/spotify"/></spot:external_urls_spotify>
                            <spot:href><xsl:value-of select="href"/></spot:href>
                            <spot:id><xsl:value-of select="id"/></spot:id>
                            <spot:type><xsl:value-of select="type"/></spot:type>
                            <spot:uri><xsl:value-of select="uri"/></spot:uri>
                        </rdf:Description>
                    </spot:artists>
                </xsl:for-each>

                <xsl:for-each select="track/album">
                    <xsl:variable name="id"><xsl:value-of select="id"/></xsl:variable>
                    <spot:album>
                        <rdf:Description rdf:about="http://www.recently-played-by-user.com/album/{$item}/{$id}">
                            <foaf:href><xsl:value-of select="href"/></foaf:href>
                            <spot:name_album><xsl:value-of select="name"/></spot:name_album>
                            <spot:id><xsl:value-of select="id"/></spot:id>
                            <spot:album_type><xsl:value-of select="album_type"/></spot:album_type>
                        </rdf:Description>
                    </spot:album>
                </xsl:for-each>

                <xsl:for-each select="track/album/images/item">
                    <xsl:variable name="size"><xsl:value-of select="width"/></xsl:variable>
                    <spot:image>
                        <rdf:Description rdf:about="http://www.recently-played-by-user.com/image/{$item}/{$size}">
                            <foaf:url><xsl:value-of select="url"/></foaf:url>
                            <spot:width><xsl:value-of select="width"/></spot:width>
                            <spot:height><xsl:value-of select="height"/></spot:height>
                        </rdf:Description>
                    </spot:image>
                </xsl:for-each>

                <xsl:for-each select="track/album/artists">
                    <xsl:variable name="id"><xsl:value-of select="id"/></xsl:variable>
                    <spot:artists_album>
                        <rdf:Description rdf:about="http://www.recently-played-by-user.com/artists/{$item}/{$id}">
                            <foaf:name><xsl:value-of select="name"/></foaf:name>
                            <spot:external_urls_spotify><xsl:value-of select="external_urls/spotify"/></spot:external_urls_spotify>
                            <spot:href><xsl:value-of select="href"/></spot:href>
                            <spot:id><xsl:value-of select="id"/></spot:id>
                            <spot:type><xsl:value-of select="type"/></spot:type>
                            <spot:uri><xsl:value-of select="uri"/></spot:uri>
                        </rdf:Description>
                    </spot:artists_album>
                </xsl:for-each>
            </rdf:Description>
    </xsl:template>

</xsl:stylesheet>